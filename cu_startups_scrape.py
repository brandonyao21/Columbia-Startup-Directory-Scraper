from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import regex as re
import time

LIMIT = 100

pageNum = 0


driver = webdriver.Firefox()
driver.maximize_window()
company_list = []

for i in range(0,LIMIT):
    print(i)
    link = f"https://startups.columbia.edu/startups?page={i}&sort=latest_update"
    driver.get(link)
    time.sleep(5)
    cards = driver.find_elements(By.CSS_SELECTOR, "li.index-list-item  > div.organization-flex")
    #print(cards, len(cards))

    #try to scrape information from the rest
    for card in cards:
        #print(card)
        header = card.find_element(By.CLASS_NAME, "header")
        desc = card.find_element(By.CLASS_NAME, "description")
        desc = desc.text if desc else None
        name = (header.find_element(By.CSS_SELECTOR, "div.name > a")).text
        print(name)
        subs = header.find_elements(By.CLASS_NAME, "subtitle")
        founding_yr = None
        total_raised = None
        for sub in subs:
            spans = sub.find_elements(By.CSS_SELECTOR, "span")
            #print(spans)
            for span in spans:
                txt = span.text
                #print(txt)
                funds = re.search("\$([\d|.]*[M|K])",txt)
                if funds:
                    num = funds.group(1)
                    total_raised = (1e6 if num[-1] == 'M' else 1e3)*float(num[:-1])

                yr = re.search("(\d\d\d\d)", txt) 
                if yr:
                    founding_yr = int(yr.group(1))   
        card_row = [name, desc, founding_yr, total_raised]
        company_list.append(card_row)
#lets save this
df = pd.DataFrame(company_list, columns=["Name", "Description", "Founding Year", "Total Funding"])

no_na = df.dropna(axis=0)
df.fillna("N/A")
df.to_csv("./data/full_table.csv")
target = no_na[(no_na["Founding Year"].astype(int) >= 2022) & (no_na["Total Funding"].astype(int) <= 5e6)]
target.to_csv("./data/target_table.csv")