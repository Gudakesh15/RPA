# -*- coding: utf-8 -*-
"""
Conan Jr
- a crawler aspiring to be generic, raw, and a bit brutal with German DNA

Created on Thrus August 20

@author: Aviral

-implement test mode

Additions:

1. Separation Of Concern Implementation
2. Agrv function for user_agents' Updation
3. Additional 200 check
"""

import requests
import csv
import os
import tarfile
import datetime

"""
This function 1 is to set a user agent and update the dictionary with the choosen one
"""

def setUserAgent(pick):
    global s
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36']
    s.headers.update({'user-agent':user_agents[pick%len(user_agents)]})
   
"""
This function 2 is to set a proxy and update the dictionary with the choosen one
"""
   
def setProxy(locInt):
    global s
    global proxyLoc
    
    if locInt%2 == 0:
        proxies = {"https":"https://wayf:Mse5q12Gze@wayf.shader.io:60002"}
        s.headers.update({'accept-language':'en-US,en;q=0.9,es;q=0.8,de;q=0.7,fr;q=0.6,it;q=0.5'}) #NOTE: IT IS CLEVER TO STORE THE USER_AGENTS ELEMENT IN A DICTIONARY. THIS WAS YOU CAN UPDATE ALL OF THEM INDIVIDUALLY.
        proxyLoc = 'UK'
    elif locInt%2 == 5:
        proxies = {"https":"https://lum-customer-wayfair-zone-static-country-fr:4sz14id93909@zproxy.lum-superproxy.io:22225"}
        s.headers  = {'accept-language': None}
        proxyLoc = 'FR'
            
    else:
        proxies = {"https":"https://wayf:Mse5q12Gze@wayf.shader.io:60001"}
        s.headers.update({'accept-language':'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6,es;q=0.5'})
        proxyLoc = 'DE'
            
        s.proxies = proxies #changing the proxy in the dictionary
        
"""
This function 3 is to check if a connection is being established to the website
"""
        
def crawlURL(path):
    attempts=0
    pageContent= ''
    global s
    while attempts <5:
        try:
            pageContent = s.get(url_path).text
            attempts = 10 #dummy break condition added so that once we connect to the page we don't retry again and again
        except:
            attempts += 1; #if we do not connect however, the number of attempts will be incremented
            print('crawl error URL')
    return pageContent
    
"""
this function is to implement Separation of concern by setting the needful for the first 3 functions
"""
def SettingState():
    #global s = requests.Session()
    pl = 3 #since the remainder won't be in (0,5), it will use language
    setProxy (pl)
    setUserAgent (10)
    
    url_path = 'https://www.bild.de/kreditkarten/visa-oder-mastercard/'
    
    pageContent = crawlURL(url_path)
    
SettingState()
    
    
    
        
        
    
    


