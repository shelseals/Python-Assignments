
# coding: utf-8

#Shelby Jennings, ssj2124
#IEOR4571 Web Scraping Assignment

import re
from urllib.robotparser import RobotFileParser 
import requests
from bs4 import BeautifulSoup
import bs4
#Not importing time because this scraper object doesn't need to pull data from site over and over when ran 

#This class scrapes the website of Barnard College to collect updated info on school's website
class BarnardScraper():
    def __init__(self): 
        self.data = {}
        
    def scrape(self):
        #Returns results of the 2 method objects 
        top_stories = self.get_top_stories() 
        #print(self)
        social_media = self.get_social_media()
        print("Top stories on Barnard.edu: ")
        print(top_stories)
        print("Barnard College social media accounts: ")
        print(social_media)
        
    def get_top_stories(self): #These are the stories on the site's hompage slideshow on a given day      
        url = 'https://www.barnard.edu/robots.txt'
        rfp = RobotFileParser(url=url)
        rfp.read()
        if not rfp.can_fetch('*', url): #Making sure Barnard allows this 
            raise RuntimeError('Barnard disallows')        
        req = requests.get('https://www.barnard.edu')
        soup = BeautifulSoup(req.text, 'lxml')

        top_stories = {}
        #The title page stories come in 3 formats, either https, http or as part of homepage slideshow
        #but connecting to another link on site, 3 for loops account for each case to pull
        #all potential top stories from page
        for tag in soup.find_all('a', href=re.compile('https://www\.barnard\.edu/news/')):
            top_stories[tag.get_text()] = tag.get('href')
        for tag in soup.find_all('a', href=re.compile('http://barnard\.edu/news/')):
            top_stories[tag.get_text()] = tag.get('href')
        for tag in soup.find_all('a', href=re.compile('homepage-slideshow')):
            top_stories[tag.get_text()] = tag.get('href')   
        
        final_top_stories = {}
        #The above url's also appear in other unwanted places
        #so this for loop eliminates any case that isn't actually a top story but 
        #whose tag contains "top story information" for another reason 
        for key in top_stories:
            if key != '' and key != '\n':
                final_top_stories[key] = top_stories[key]
        return final_top_stories


    def get_social_media(self): #Finding links to Barnard's social media profiles; these should not change 
        url = 'https://www.barnard.edu/robots.txt'
        rfp = RobotFileParser(url=url)
        rfp.read()
        if not rfp.can_fetch('*', url): #Making sure Barnard allows this 
            raise RuntimeError('Barnard disallows')        
        req = requests.get('https://www.barnard.edu')
        soup = BeautifulSoup(req.text, 'lxml')
        
        social_media = []
        #Searching through all url tags to find those of class ['footer-Facebook']
        # or ['footer-Youtube'], etc. to create list of all social media accounts 
        for tag in soup.find_all('a'):
            if type(tag.get('class')) != "<class 'NoneType'>" and tag.get('class') != None:
                for element in tag.get('class'):
                    if element.startswith('footer-'):
                        link = tag.get('href')
                        social_media.append(link)
        return social_media
    
#I = BarnardScraper()
#print(I.scrape()) 

