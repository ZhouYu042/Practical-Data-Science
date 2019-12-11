import io, time, json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random

# source code from course homework
# Args: url (string):
# Returns: status_code (integer), raw_html (string)
def retrieve_html(url):
   
    response = requests.get(url)
    status = response.status_code
    content = response.text
    
    return (status, content)

def read_api_key(filepath="api_key_clear.txt"):
    return Path(filepath).read_text().strip()


# Make an authenticated request to the Yelp API, modified from 
# Args:  query (tuple): (latitude, longitude, radius, category)
# returns: total (integer): total number of businesses on Yelp corresponding to the query 
#          businesses (list): list of dicts representing each business
def yelp_search(api_key, query):
        
    header =  {'Authorization': 'Bearer '+ api_key}
    url = "https://api.yelp.com/v3/businesses/search"
    searchKey = dict()
    
    
    lat, long, radius, cat = query
    
    searchKey["latitude"] = lat
    searchKey["longitude"] = long
    searchKey["radius"] = radius
    searchKey["categories"] = cat
    
    searchKey["sort_by"] = "distance"
    searchKey["location"] = "Pittsburgh"
    
    response = requests.get(url, params=searchKey, headers=header)
     
    
    business = []
    
    responseDict = json.loads(response.text)
    
    if "businesses" in responseDict:
        business = responseDict["businesses"]
        
    total = responseDict["total"]
    
    return total, business


# Get average rating and price level of business list
# Args: total: total (integer): total number of businesses
#       businesses (list): list of dicts representing each business
# Returns: average_rating(float), average_price(float)
def get_average(total, business):
    
    ratings = 0
    prices = 0
    rating_count = 0
    price_count = 0
    res_rating = 0
    res_price = 0
    
    for res in business:

        if "rating" in res:
            rating = res["rating"]
            ratings += rating
            rating_count += 1
        
        
        if "price" in res:
            price = res["price"]
            prices += len(price)
            price_count += 1
            
    if rating_count != 0:
        res_rating = ratings / rating_count
        
    if price_count != 0:
        res_price = prices / price_count
    
    if total == 0:
        return 0, 0
        
    return res_rating, res_price

# Fill in nearby restaurant information for each house in the database
def get_restaurant():
    for i in range(len(df)):
        lat, long = df.loc[i,["latitude", "longitude"]]
        query = (lat, long, 1000, "restaurants")
        total, business = yelp_search(api_key_clear, query)
        rating, price = getAverage(total, business)
        df.loc[i, "count_1000"] = total
        df.loc[i, "rating_1000"] = rating
        df.loc[i, "price_1000"] = price
        time.sleep(0.5)
        if i % 100 == 0:
            time.sleep(random.randint(1, 3))

# Fill in nearby art and entertainment count for each house in the database
def get_arts():
    for i in range(5339, len(df)):
        lat, long = df.loc[i,["latitude", "longitude"]]
        query = (lat, long, 1500, "arts")
        total, business = yelp_search(api_key_clear, query)
        if total != 0:
            count = 0
            for item in business:
                dis = item["distance"]
                if dis <= 1500:
                    count += 1
                else:
                    break

            df.loc[i, "arts_f"] = count

        df.loc[i, "arts"] = total

        time.sleep(0.5)

        if i % 100 == 0:
            time.sleep(random.randint(1, 3))


# Fill in nearby groceries count for each house in the database
def get_grocery():
    for i in range(len(df)):
        lat, long = df.loc[i,["latitude", "longitude"]]
        query = (lat, long, 1500, "grocery")
        total, business = yelp_search(api_key_clear, query)
        if total != 0:
            count = 0
            for item in business:
                dis = item["distance"]
                if dis <= 1500:
                    count += 1
                else:
                    break

            df.loc[i, "grocery_f"] = count

        df.loc[i, "grocery"] = total

        time.sleep(0.5)

        if i % 100 == 0:
            time.sleep(random.randint(1, 2))


def main():
    global df
    path = "scrape_trulia_list.csv"
    df = pd.read_csv(path)
    names = ["streetAddress", "postalCode", "latitude", "longitude", "link"]
    df = df[names]
    # df.head

    # Initialize colunms for nearby restaturants information
    radius = 1000
    df["count_%d"%r] = np.nan
    df["rating_%d"%r] = np.nan
    df["price_%d"%r] = np.nan

    get_restaurant()

    # Inititalize columns for arts and grocery
    df["arts"] = np.nan
    df["arts_f"] = np.nan
    df["grocery"] = np.nan
    df["grocery_f"] = np.nan

    get_arts()
    get_grocery()


    df.to_csv("yelp_res.csv")


if __name__ == '__main__':
    main()
