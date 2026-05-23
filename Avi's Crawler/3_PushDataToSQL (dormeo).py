 """
Review by Aviral
Reviewed on Thurs Aug 20

Review:

1. Does sqlalchemy create performance issues as the layer of abstraction reduces efficiency? 
2. All the configurations can be stored in a separate file or a .env file 
where all the configurations would have been updated only once
3. The directory for storing the files can be linked to a global variable which can be changed when handing over the files to
new users

"""

 
 
 # import relevant libraries
import pandas as pd
import datetime as dt
import sqlalchemy #sql package used to read data and input data into CRUD: Create, read, update, delete. ORM converts table into object: Object Relational Mapping
#sqlalchemy does ORM stuff. This however creates performance issues as you are not using raw sql
#sqlalchemmy is one of many ORMs. SQLalchemy is build on the concepts ORM. It will read it as if it were an object
import os
import pyodbc
import datetime
dn = datetime.datetime.now();

def read_query(query_file): #reading a sql file. 

    """ reads sql query from .sql file into a python variable """

    with open(query_file + '.sql', 'r') as query_file_contents:
        my_query = query_file_contents.read()

    return my_query #Storing sql file in a python variable

def connect_sql(driver_name, server_name, db_name): #this whole line is called signature of the function

    """ Opens and returns a connection instance (via a cursor object) to sql server """

    print('----------Connecting to SQL')

    # fill in connection string w/ driver (search ODBC Data Sources on your computer), server (sqlboadhoc,sqlcompintelro,etc), database (can specify ANY db in server. just a starting pt) 
    connection = pyodbc.connect("DRIVER={" + driver_name + "}; SERVER=" + server_name
        + "; DATABASE=" + db_name + "; Trusted_Connection=yes;MultiSubnetFailover=Yes;autocommit=True")

    # initialize cursor object -> the thing that allows you to actually execute sql thru the above connection 
    cursor = connection.cursor() #a non visual indicator saying that connection has been established. If connection failed then query will fail here
    
    print('----------Connection Opened')

    return cursor, connection

def select_sql(cursor, sql): #takes in cursor and sql: is a basic sql statement
    

    """ Emulates a SELECT statement, intaking a query and generating a pd df """ 

    print('----------Selecting SQL')

    # use cursor object to execute sql statement
    cursor.execute(sql) #after execution we get a table

    print('----------Generating DataFrame')
    
    # generate list of column headers
    column_list = [column[0] for column in cursor.description] #storing the name of the columns in the table

    # iteratively populate list of lists signifying each record in table
    row_list = [row for row in cursor] #storing the name of the rows in the table

    # generate pd df using col_list and row_list
    table = pd.DataFrame.from_records(row_list, columns=column_list)
    
    print('----------DataFrame Generated')
    
    return table
    #storing the results of the query in a variable

def update_sql(cursor, connection, sql): #updating data in a specified table

    """ Executes NON-"SELECT" sql statements. Used to run queries that will, say, update junk tables """  

    print('----------Updating SQL')
    print('   Starting Process - {}'.format(dt.datetime.now())) #prints the start time

    # use connected cursor object to run the query
    cursor.execute(sql)
    connection.commit() #saving the updatesd data in the database

    print('   Process Complete - {}'.format(dt.datetime.now())) #prints the end time

    return None

def push_sql(driver, server, database, dataframe, table): #adding new df (dataframes aka tables) into server you find something new

    """ Pushes pd dfs into SQL Server tables """

    print('----------Pushing to SQL Table: {}'.format(table))
    print('    Starting Process - {}'.format(dt.datetime.now()))

    # fill in connection string w/ driver (search ODBC on computer), server, database (any db, just starting pt) 
    conn_string = 'mssql+pyodbc://' + server + '/' + database + '?trusted_connection=yes&driver=' + driver + '&autocommit=true'

    # use sqlalchemy to create an "engine" driven by your connection parameters and connect
    engine = sqlalchemy.create_engine(conn_string, isolation_level='READ_UNCOMMITTED') #enabling sqlalchemy to connect to the dfs
    connection = engine.connect() #same thing like cursor

    # command to push dataframe to sql table
    dataframe.to_sql(table, con=connection, if_exists='append', index=False, schema='dbo', chunksize=1000)


    # close connection
    connection.close()

    print('    Process Complete - {}'.format(dt.datetime.now())) #timestamps

    return None

def close_sql(cursor, connection):
    
    """ Close connection & delete cursor object to free up sql server resources """
    
    print('----------Closing SQL Connection')

    del cursor
    
    connection.close()
    
    print('----------Connection Closed')

    return None

# specify sql server connection parameters
# these are all configurations. Can have it in one single file
#from here 
s_driver = 'ODBC Driver 13 for SQL Server'
s_c_server = 'SQLCOMPINTELRO'
s_database = 'csn_junk'

sourceName='AppliancesDirect'

os.chdir('C:/Users/lv520b/Documents/') #these are users. could have made an intern variable. Now we have to update ever line. 
#could have made an intern path which could have changed in configure file. 
#could have had a configuration file where all the configurations would have been updated only once. 
#till here could be in configuration file or .env file environment varibales
#Dormeodf1 = pd.read_excel('%02d%02d%02dDormeo_scrape.xlsx'%(dn.year,dn.month,dn.day))
df1 = pd.read_excel('%02d%02d%02dDormeo_scrape.xlsx'%(dn.year,dn.month,dn.day))
#df=df1.drop(columns='Unnamed: 0')

 # connect to 2 separate sql servers (w_ = sqlboadhoc, c_ = sqlcompintelro)
c_cursor, c_connection = connect_sql(s_driver, s_c_server, s_database)

#push dataframe to SQL Junk table

push_sql(s_driver, s_c_server, s_database, df1, 'tbldormeotest')

# close connection to each sql server
close_sql(c_cursor, c_connection)