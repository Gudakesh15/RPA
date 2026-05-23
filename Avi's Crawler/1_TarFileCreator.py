# -*- coding: utf-8 -*-
"""
Review of Conan v0 by Aviral


Created on Wed July 10 
Reviewed on Thurs Aug 20

@author: jdobrindt

- implement test mode

Review:

1. Separation of Concern can be integrated in this file
2. By importing sys, a file with new User_Agents can be passed to the script, for updating purposes.

Example of the code:     

if len(sys.argv) > 1:
        setUserAgent_updated(pick): #chooses a User Agent from the file passed through command line
    else:
        setUserAgent(pick): #chooses a User Agent from the list in the script
3. Addition of raise_for_status() after s.get will help us ensure that the download has actually 
worked before your program continues.

Example of the code: 

try:
    pageContent.raise_for_status() 
except Exception as exc:
    print('There was a problem: %s' % (exc))

4. Implementing consistency in naming convention. Name all the functions in camel casing or snake casing. 
Eg: pageContent is camel casing whereas url_path is snake casing


"""

import requests
import csv
import os
import tarfile
import datetime

def setUserAgent(pick):
    global s # s is an object/variable
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36']
    s.headers.update({'user-agent':user_agents[pick%len(user_agents)]})


def setProxy(locInt):
    global s
    global proxyLoc
    
    if locInt%2 == 0:
        proxies = {"https":"https://wayf:Mse5q12Gze@wayf.shader.io:60002"} # PROXY UK
        s.headers.update({'accept-language':'en-US,en;q=0.9,es;q=0.8,de;q=0.7,fr;q=0.6,it;q=0.5'})
        proxyLoc = 'UK'
    elif locInt%2 == 5:  # condition that cannot be fulfilled to take the French proxy out
        proxies = {"https":"https://lum-customer-wayfair-zone-static-country-fr:4sz14id93909@zproxy.lum-superproxy.io:22225"} # PROXY FR
        s.headers  = {'accept-language': None}
        #s.headers.update({'accept-language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5'})
        proxyLoc = 'FR'
    else:
        proxies = {"https":"https://wayf:Mse5q12Gze@wayf.shader.io:60001"} # PROXY DE
        s.headers.update({'accept-language':'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6,es;q=0.5'})
        proxyLoc = 'DE'
    s.proxies = proxies
     
    
def crawlURL(path): 
    attempts=0
    pageContent=''
    global s
    while attempts<5:
        try:
            pageContent = s.get(url_path).text 
            attempts = 10 # dummy break condition
        except:
            attempts+=1;    
            print('crawl error URL') 
    return pageContent #this is camel case


def writeToTar(path,text):

    global tar_handle
    with open(path+'.html','w',encoding='utf8') as tempFile:
        tempFile.write(text)
    tempFile.close()
    
    tar_handle.add(path+'.html')
    os.remove(path+'.html')

sourceName='Dormeo'

os.chdir('C:/Users/lv520b/Documents/')
URLlist='sitemapdormeo.txt'
dn = datetime.datetime.now(); #when was it made (timestamp)
TarOut='%02d%02d%02d%s.tar.gz'%(dn.year,dn.month,dn.day,sourceName) #giving the file a name and giving it an extension making it human readable


testmode=0
sizeLimit=1e5

if testmode!=1:
    tar_handle=tarfile.open(TarOut,'w:gz')

s = requests.Session()
pl=3 # proxy language, uing DE
setProxy(pl)
setUserAgent(10)
padding='0000000000' # this is used for zero padding of the filename


#s.headers.update({'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/web'})
#s.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})

URLs=[]
with open(URLlist,'r') as URLfile:
    csv_reader = csv.reader(URLfile, delimiter='\t') # delimation is the difference. \t is a tab. obejcts are seprated by tabs. csv file has proper deliminators
    for row in csv_reader:
        URLs.append(row)
URLfile.close()
    
blocked_urls=[]

if testmode==1: #if test mode has been changed to 1 then crawl limit has been set to 10
    crawlLimit=10
else:
    crawlLimit=len(URLs) #or else crawl limit = to the number of urls
    

for i in range(crawlLimit): 
#for i in blocked_urls: #<-- check and recrawl blocked URLs
        
    url_path=URLs[i][1]   #2D array. #put a print statement
    surlID=URLs[i][0] #every column's first row has surlID
    surlComp=URLs[i][2]    #every column's second row has surlComp
    
#    url_path=URLs[0][1] # for testing
#    surlID=URLs[0][0]
#    surlComp=URLs[0][2] 
    
    # crawl URL
    pageContent=crawlURL(url_path)
        
    # try one proxy switch
    if len(pageContent)<sizeLimit:
        print('blocked')
        pl+=1 #if they are blocked then proxy is changed
        setProxy(pl)
        setUserAgent(i)
        print('Proxy switched to '+proxyLoc)
        # FOR FUTURE VERSION: WAIT 120s AFTER BEING BLOCKED
        pageContent=crawlURL(url_path)
    
    # record url as blocked if proxy switch did not resolve the problem
    if len(pageContent)<sizeLimit:   
        print('blocked again - no retry')
        #blocked_urls.append(i)
        blocked_urls.append(url_path)
           
    out_path = padding[:-len(surlID)]+surlID+'_'+surlComp    
    print(out_path)
    print( '%d' % len(pageContent))
        
    if testmode!=1:
        writeToTar(out_path,pageContent)
        

tar_handle.close()   