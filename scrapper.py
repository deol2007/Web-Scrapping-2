from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import requests
import pandas as pd

#nasa's expo planet url
START_URL="https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

#web driver
browser=webdriver.Chrome("C:/Users/raman/webScrapping/chromedriver")
browser.get(START_URL)

#make system sleep until all the data is accessed
time.sleep(10)

planet_data=[]

#new variable for organising data
headers=["Star","Constellation","Right ascension","Declination", "Apparent magnitude","Distance","Spectral type","Mass", "Orbital Period","Semimajor axis", "Eccentricity"]

def scrape():
    for i in range (1,5):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")

            #checking page number
            current_page_num=int(soup.find_all("input",attrs={"class", "page_num"})[0].get("value"))

            if current_page_num <i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num >i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul",attrs={"class", "expoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)

            #get hyperlink tag
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"Page {i}: Scrapping Completed!")

#calling method
scrape()

new_planets_data=[]

def scrap_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)
#calling method using for loop to check new_planets_data
for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f"Scraping at Hyperlink {index+1} is Completed!")

print(new_planets_data[0:10])
final_planet_data=[]

for index,data in enumerate(planet_data):
    new_planets_data_element=new_planets_data[index]
    new_planets_data_element=[elem.replace("\n","") for elem in new_planets_data_element]
    new_planets_data_element=new_planets_data_element[:7]
    final_planet_data.append(data+new_planets_data_element)

with open("final.csv","w") as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)