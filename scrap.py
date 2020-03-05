from bs4 import BeautifulSoup
import os
import requests
import time
import sys
import json


def extract_doc(rev,company):
        #Doc dict
        doc = {}
    
        doc["company"] = company
    
        #Review id
        doc["review_id"] = rev['data-review']
  
        #Review epoch date
        doc["date"] = time.strftime('%d/%m/%Y', time.localtime(int(rev['data-date'])))
   
        #Review language
        doc["language"] = rev['data-language']
    
        #Review header
        doc["title"] = rev.find("h3", class_="review_header").text.strip()
    
    
        #Retrieve content
        content_raw = rev.find("div", class_="review-summary")\
                        .find("div", class_="toggle-content")
    
        #Cleanup tags
        for tag in content_raw.find_all('a'):
            tag.replaceWith('')
        for tag in content_raw.find_all('span'):
            tag.replaceWith('')

        doc["content"] = content_raw.text.replace("\r", "")\
                                         .replace("\t", "")\
                                         .replace("\n", "")\
                                         .strip()
    
        #Retrieve scoring
        doc["overall_rating"] = float(rev.find("div", class_="review-rating")\
                                         .find("span", class_="review-score").text)
    
        #Retrieve various scoring
        ratings = rev.find("ul", class_="user_review_rating_list")\
                     .find_all("div",class_="stars-rating")

        #Rating details
        doc["reliability_rating"] = float(ratings[0]['data-rating'])
        doc["pricing_rating"] = float(ratings[1]['data-rating'])
        doc["user_friendly_rating"] = float(ratings[2]['data-rating'])
        doc["support_rating"] = float(ratings[3]['data-rating'])
        doc["features_rating"] = float(ratings[4]['data-rating'])   

        return doc


#Write to file
def write_json(doc_array,company):
    
    with open("/scrap_data/"+company+'.json', 'w') as json_file:
        json.dump(doc_array, json_file)


def main():
        # print command line arguments
        if len(sys.argv[1:]) != 1:
            print("Usage : python3 scrap.py url")

        url = sys.argv[1]

        #Array that will contain all reviews
        doc_array = []

        #Test page
        base_url = url+"page/"

        current_page = 1
        page = requests.get(base_url+str(current_page))

        #Test page existence
        if page.status_code == 404:
            return 1

        #Retrieve number of pages for that company to loop on it
        soup = BeautifulSoup(page.content,'html.parser')
        try:
            num_links = int(soup.find_all("a",class_='page-numbers')[-1].text)
        except:
            num_links=1

        #Retreive company name from url
        company = base_url.split("/")[4].replace("-reviews","")

        #Loop on pages list
        for current_page in range(1,num_links+1):

            #TODO REPLACE WITH LOGGING
            print(str(current_page)+"/"+str(num_links))

            #Parse page content for reviews 
            page = requests.get(base_url+str(current_page))
            soup = BeautifulSoup(page.content,'html.parser')
            review_contents = soup.find_all("article",class_="user_review_holder")

            for rev in review_contents:
                #Extract reviews in json format
                doc = extract_doc(rev,company)
                doc_array += [doc]

        #Write down to file
        write_json(doc_array,company)


if __name__ == "__main__":
    main()
