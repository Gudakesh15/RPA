# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:22:26 2020
Reviewed on Thurs Aug 20

@author: sz899x
Reviewd by: Aviral

1. Great implementation for differentiating between test mode and production mode
2. Good suboptimization
3. Efficient storing of data
4. Good check for PDP page


"""

import os 
import tarfile
from bs4 import BeautifulSoup
import re 
import pandas as pd
import datetime
dn = datetime.datetime.now();
testMode=0

sourceName='Dormeo'

os.chdir('C:/Users/lv520b/Documents/')
dict_list=[]
count=0

print('extracting file list from tar...')
tf = tarfile.open('%02d%02d%02d%s.tar.gz'%(dn.year,dn.month,dn.day,sourceName))
fileList=tf.getmembers() #getting the list of the files inside a tar folder
print('done')

if testMode==1: #only set when they are testing the code. This is enabled when they are testing stuff
    for f in fileList:
        count+=1
        if count>10:
            break
        tf.extract(f) # this extracts the actual file

else:  #this is when the code in running in production
    for f in fileList:
                
        count+=1
        #f=fileList[77]
        filePath=f.name # this stores the filename
        tf.extract(f) # this extracts the actual file
        
        # reading the extracted file
        with open(filePath,'rt', encoding='utf8') as fileIn:
            pageContent=fileIn.read()
            fileIn.close()
        # removing the extracted file
        os.remove(filePath)
        url_id=str(int(filePath[:10])) #storing uptill 10 characters of url id
        if count%100==0: #rare case
            print(str(count)+'. file read ('+url_id+')')

# preparing soup...
        soup = BeautifulSoup(pageContent, 'html.parser') # unzipping and parsing

#Regular Expression
        soupString = str(soup)
# https://regex101.com/ #regular expression to find patters in text

# important to note that the number of JSONs vary depending on the page. Product detail pages have 3 JSONs while pages that are not PDP have only 2.
# pages with product options but which are not PDP themselves also have 3 JSONs so that has to be taken into account as well.
        
        try:    
            pdp_check = re.findall(r'<script type="application/ld\+json">(.*?)</script>', soupString)[2].find('"price"')
        except:
            pdp_check = -1 #price can never be -1
            
        if pdp_check==-1:
            print(f.name + ' is not a PDP!')

        if pdp_check>=0:

#opening dictionary to collect data
            
            import json #this is sub optimisation. 
            import pyperclip
            pyperclip.copy(soupString)
            
            itemsJSON=re.findall(r'<script type="application/ld\+json">(.*?)</script>', soupString)
            itemsJSONbreadcrumb=itemsJSON[0]
            itemsJSONproduct=itemsJSON[2]
                       
            jsonObjBreadcrumb = json.loads(itemsJSONbreadcrumb)
            jsonObjProduct = json.loads(itemsJSONproduct)
            
            #when they verified the page they are storing all the information
            #API: api has 4 inputs: get put(updating) post(storing) delete
            #Full form of API: Application interface programing

            attributes={}
            attributes['CpuURL']=jsonObjProduct['url'] #value is a json object
            attributes['CppProductName']=jsonObjProduct['name']
            attributes['CppOptionName']=jsonObjProduct['name']
            attributes['CppProductDescription']=jsonObjProduct['description']
            attributes['CppProductImage']=jsonObjProduct['image']
            attributes['CppPrice']=jsonObjProduct['offers'][1]['price']
            attributes['CppCurrency']=jsonObjProduct['offers'][1]['priceCurrency']
            attributes['CppManufacturer']=jsonObjProduct['offers'][1]['seller']['name']
            attributes['CppPartNumber']=jsonObjProduct['mpn']
            attributes['cppBreadCrumb']=jsonObjBreadcrumb['itemListElement'][0]['item']['name']
             #trying to find the features
            try:
                attributes['CppParentIdentifier']=soup.find("input", {"name" : "product"}).get("value")
            except:
                attributes['CppParentIdentifier']=''
            attributes['CppChildIdentifier']=jsonObjProduct['sku']
            attributes['cppQuantity']=jsonObjProduct['offers'][1]['availability'].split('/')[3]                        
            try:
                attributes['cppSpecs']=soup.find("div", {"class" : "features-list__list"}).text
            except:
                attributes['cppSpecs']=''
            attributes['CppProductCategory']='Mattresses and Beds'

            #trying to find rating
            try:
                attributes['CppProductRating']=soup.find("span", {"class" : "bvseo-ratingValue"}).text
            except:
                attributes['CppProductRating']=''
            dict_list.append(attributes)
                                             
tf.close()

if testMode!=1:
    print('Converting to excel...')
    csd_table = pd.DataFrame(dict_list)
    csd_table.to_excel('%02d%02d%02dDormeo_scrape.xlsx'%(dn.year,dn.month,dn.day), sheet_name='Catalog')
    csd_table.to_csv('%02d%02d%02dDormeo_scrape.csv'%(dn.year,dn.month,dn.day))

    #test mode is a global variable. test mode when set to != 1 will not print unnessary stuff