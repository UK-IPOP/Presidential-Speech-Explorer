#Import requests, Beautiful Soup, Pandas, and Path
import requests, bs4, pandas as pd 
from pathlib import Path

#Enter keyword to be searched as a string
keyword = ""

#American Presidency project URL with the keyword
url = 'https://www.presidency.ucsb.edu/advanced-search?field-keywords=' + keyword +'&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=&items_per_page=100'

#Set the number for the first speech on the page. This will increase as the page number increases
first_speech = 0
#Create lists to store information from the page
date_list =[]
speaker_list = []
title_list = []
speech_list = []
#Create a directory to save information
Path('Speeches').mkdir(exist_ok = True)

#Use while loop to move through pages until there is no next page
while  True:
    
    #Request the webpage
    res = requests.get(url)
    #Check the page was downloaded sucessfully
    res.raise_for_status()

    #Create a BeautifulSoup object
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    #Find the dates of the speeches linked in the page. This will also give the number of speeches on the page
    dates = soup.select('.views-field.views-field-field-docs-start-date-time-value.text-nowrap')
    #Find the speakers
    speaker = soup.select('td.views-field.views-field-field-docs-person a')
    #Find the titles of the speeches
    title = soup.select('td.views-field.views-field-title a')

    #Create a loop to store information for each speech in the lists created above
    for i in range(len(dates)):
        date_list = date_list + [dates[i].getText().strip()]
        speaker_list = speaker_list + [speaker[i].getText().strip()]
        title_list = title_list + [title[i].getText().strip()]
        #Find links for the texts of the speeches and add them to the speech_list
        speech_page = 'https://www.presidency.ucsb.edu' + title[i].get('href')
        speech_list = speech_list + [speech_page]
        #Request the speech page
        speechrequest = requests.get(speech_page)
        #Check the page was downloaded sucessfully
        speechrequest.raise_for_status()
        #Create a BeautifulSoup object for the speech page
        speech_soup = bs4.BeautifulSoup(speechrequest.text, 'html.parser')
        #Get the text of the speech
        content = speech_soup.select('.field-docs-content')[0].getText()
        
        #write the content to a text file named with the index of the speech in the dataframe
        with open('Speeches/{0}.txt'.format(i + first_speech), 'w') as f:
            f.write(content)
    #add to the first_speech number
    first_speech = first_speech + 100
    #Find the next page
    try:
        nextpage = soup.select('.next a')[0]
    #Go to the next page
        url = 'https://www.presidency.ucsb.edu' + nextpage.get('href')
    except:
        break

#Create a dataframe
df = pd.DataFrame({'Date' : date_list, 'Speaker' : speaker_list, 'Title' : title_list, 'Link' : speech_list})

#Write dataframe to csv
df.to_csv('Speeches/speeches.csv')