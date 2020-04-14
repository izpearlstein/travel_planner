from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import re
import pygsheets
import os.path 

city_input = input("City: ")

city = city_input.replace(' ', '-').lower()

# URLs of page to be scraped
conde_nast_restaurants_url = 'https://www.cntraveler.com/gallery/best-restaurants-in-{0}'.format(city)
conde_nast_activities_url = 'https://www.cntraveler.com/gallery/best-things-to-do-in-{0}'.format(city)
conde_nast_hotels_url = 'https://www.cntraveler.com/gallery/best-hotels-in-{0}'.format(city)

# Conde Nast Restaurants Retrieval
response = requests.get(conde_nast_restaurants_url)
soup = bs(response.text,'html.parser')

results = soup.find_all('div', class_="image-content-container")

if len(results) == 0:
    print("No data found for " + city_input )
    sys.exit()
else: pass

restaurant_list = []
price_list = []
blurb_list = []

for result in results:
    try:
        restaurant = result.find('h2', class_='hed').text
        price = result.find('p', class_='price').text
        blurb = result.find(class_='dek').text
        if (restaurant and price and blurb):
            restaurant_list.append(restaurant)
            price_list.append(price)
            blurb_list.append(blurb)
    except AttributeError as e:
        print(e)
        
restaurants = pd.DataFrame(list(zip(restaurant_list, price_list, blurb_list)), 
               columns =['Restaurant', 'Price', 'Description'])

# Conde Nast Activities Retrieval
response2 = requests.get(conde_nast_activities_url)
soup2 = bs(response2.text,'html.parser')
results2 = soup2.find_all('div', class_="image-content-container")

if len(results2) == 0:
    print("No data found for "+ city_input)
    sys.ext()
else: pass

activity_list = []
blurb_list = []

for result in results2:
    try:
        activity = result.find('h2', class_='hed').text
        blurb = result.find(class_='dek').text
        if (activity and blurb):
            activity_list.append(activity)
            blurb_list.append(blurb)
    except AttributeError as e:
        print(e)
        
activities = pd.DataFrame(list(zip(activity_list, blurb_list)), 
               columns =['Activity', 'Description'])

# Conde Nast Hotels Retrieval
response3 = requests.get(conde_nast_hotels_url)
soup3 = bs(response3.text,'html.parser')

results3 = soup3.find_all('div', class_="image-content-container")

if len(results3) == 0:
    print("No data found for " + city_input )
    sys.exit()
else: pass

hotel_list = []
price_list = []
blurb_list = []

for result in results3:
    try:
        hotel = result.find('h2', class_='hed').text
        price = result.find('p', class_='price').text
        blurb = result.find(class_='dek').text
        if (hotel and price and blurb):
            hotel_list.append(hotel)
            price_list.append(price)
            blurb_list.append(blurb)
    except AttributeError as e:
        print(e)
        
hotels = pd.DataFrame(list(zip(hotel_list, price_list, blurb_list)), 
               columns =['Hotel', 'Price', 'Description'])

# Export to google sheet

def df_to_gsheet(df, city_input, df_name):
    credentials = os.path.expanduser('~/New Documents/Misc/Credentials/cn-travel-planner-0746c5316afb.json') 
    gc = pygsheets.authorize(service_file=credentials)
    
    sh = gc.open('Trips')
    wks = sh.add_worksheet(city_input+'-'+df_name,rows=50,cols=6)
    wks.set_dataframe(df,(1,1))
    wks.frozen_rows = 1
    wks.cell('A1').set_text_format('bold', True)
    wks.cell('B1').set_text_format('bold', True)
    wks.cell('C1').set_text_format('bold', True)
    
df_to_gsheet(restaurants, city_input, "Restaurants")
df_to_gsheet(activities, city_input, "Activities")
df_to_gsheet(hotels, city_input, "Hotels")

credentials = os.path.expanduser('~/New Documents/Misc/Credentials/cn-travel-planner-0746c5316afb.json') 
gc = pygsheets.authorize(service_file=credentials)
sh = gc.open('Trips')
print("Updated spreadsheet here: " + sh.url)