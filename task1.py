# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:04:32 2019

@author: Abd-Elrahman
"""

import requests
from bs4 import BeautifulSoup
from time import sleep


def  getToPhilosophy(start = 'https://en.wikipedia.org/wiki/Special:Random',
                     target = 'https://en.wikipedia.org/wiki/Philosophy'):
    
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    start : str
        The URL from which we are going to start.
        
    target : str
        The URL we are hoping to reach.
        
    Returns
    -------
    list
        a list of strings representing all visited pages
    str
       determining the state of our search 'Stuck in loop', 'Stuck in no-link page', 'target reached'.
    """
    visited = []
    while start != target:
        
        #connecting to the page
        response = requests.get(start)
        sleep(0.5)
        
        #extracting the content of the page
        content = response.content
        parser = BeautifulSoup(content, 'html.parser')
        
        #find all main paragraphs in the page
        pList = parser.find_all('div', class_="mw-parser-output")[0].find_all('p', class_ = None, recursive = False)
        
        #a bool variable to determine wether we found a link or not
        findNextURL = False
        
        #loop over paragraphs
        for p in pList:
            
            #find all links of a paragraph
            linkList = p.find_all('a', href = True)

            #loop over all links
            for a in linkList:
                
                #checking if a link is valide
                if((a['href'].startswith('/wiki/') or a['href'].startswith('https://en.wiktionary.org/wiki/')) 
                and a.parent.name == 'p' and a.class_ != 'new' ):
                    
                    #extracting the text before the link
                    prevText = str(p).split(str(a))[0]
                    
                    #checking if the link is inside ()
                    if(prevText.count('(') == prevText.count(')')):
                        
                        #checking if link already visited
                        if a['href'] not in visited:
                            visited.append(a['href'])
                            start = 'https://en.wikipedia.org' + a['href'] if a['href'].startswith('/wiki/') else a['href']
                        else:
                            return 'Stuck in loop', visited
                        
                        print(start)
                        findNextURL = True
                        break
                    
            if findNextURL:
                break
            
        if not findNextURL:
            return 'Stuck in no-link page', visited
    return 'target reached', visited

print(getToPhilosophy()[1])