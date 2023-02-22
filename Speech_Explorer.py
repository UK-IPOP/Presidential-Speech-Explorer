#Import requests, Beautiful Soup, and Pandas
import requests, bs4, pandas as pd

#Enter keyword to be searched as a string
keyword = ""

#American Presidency project URL with the keyword
url = 'https://www.presidency.ucsb.edu/advanced-search?field-keywords=' + keyword +'&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=&items_per_page=100'


#Create lists to store information from page
date_list =[]
speaker_list = []
title_list = []

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

    #Create a loop to store information for each speech in the lists
    for i in range(len(dates)):
        date_list = date_list + [dates[i].getText().strip()]
        speaker_list = speaker_list + [speaker[i].getText().strip()]
        title_list = title_list + [title[i].getText().strip()]
    #Find the next page
    try:
        nextpage = soup.select('.next a')[0]
    #Go to the next page
        url = 'https://www.presidency.ucsb.edu' + nextpage.get('href')
    except:
        break

df = pd.DataFrame({'Date' : date_list, 'Speaker' : speaker_list, 'Title' : title_list})

#Write dataframe to csv
df.to_csv('speeches.csv')