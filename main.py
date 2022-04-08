import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pyperclip
import regex

#sample CIK codes to paste into the input window
#0000063908, 0000320193, 0000038009
start_time = time.time()

companies_raw = open('companies.txt', 'r')
companies = companies_raw.readlines()
print(companies)
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver/chromedriver")
driver.implicitly_wait(1)

url = "https://www.sec.gov/edgar/searchedgar/companysearch.html"

filing_records = pd.DataFrame(columns=['form_type_description',
                                       'filing_date',
                                       'reporting_date',
                                       'company_url',
                                       'company_cik'])

for company in companies:

    company = company.strip()

    driver.get(url)

    driver.find_element(By.XPATH, "//input[@id='company']").send_keys(company)

    time.sleep(.1)

    try:
        driver.find_element(By.LINK_TEXT, "No thanks").click()
        driver.find_element(By.XPATH, "//input[@id='company']").clear()
        driver.find_element(By.XPATH, "//input[@id='company']").send_keys(company)
    except:
        pass

    driver.find_element(By.XPATH, "//table[@class ='smart-search-entity-hints']").click()

    driver.find_element(By.XPATH, "//button[@id='btnViewAllFilings']").click()

    driver.find_element(By.XPATH, "//input[@id='filingDateFrom']").clear()
    driver.find_element(By.XPATH, "//input[@id='filingDateFrom']").send_keys("2000-01-01")
    driver.find_element(By.XPATH, "//input[@id='filingDateFrom']").send_keys(Keys.ENTER)

    driver.find_element(By.XPATH, "//span[normalize-space()='Copy to clipboard']").click()

    df = pyperclip.paste()
    #print(df[0])
    df = regex.sub(",", "", df)
    df = df.replace("EDGAR Entity Landing Page", "")
    df = regex.sub("Form type\s*Form description\s*Filing date\s*Reporting date\s*Filings URL",
                   "form_type_description, filing_date,	reporting_date,	file_link",
                   df)
    df = regex.sub("\n", "", df, 2)
    df = regex.sub("(?=\D[0-9]{4}-[0-9]{2}-[0-9]{2})", ",", df)
    df = regex.sub("(?<=[0-9]{4}-[0-9]{2}-[0-9]{2}\s{2})", ",", df)
    df = regex.sub("(?=https)", ",", df)
    df = regex.sub("(?<=[0-9]),\s*,(?=[0-9])", ",", df)
    df = regex.sub("(?<=[0-9]),\s,(?=h)", ",", df)

    df = df.split("\n")
    
    print(df[0])
    
    df = pd.DataFrame([row.split(",") for row in df])
    df.columns = ['form_type_description',
                  'filing_date',
                  'reporting_date',
                  'company_url']
    df = df.drop([0])
    df['company_cik'] = [company]*len(df.index)

    filing_records = pd.concat([filing_records, df])

filing_records.to_csv("posts/filings.csv")
end = time.time()
print("--- %s seconds ---" % (time.time() - start_time))

#### alternate code to just download a csv for each company (downside: many csv's)
# for company in companies:
#     driver.get(url)
#
#     driver.find_element(By.XPATH, "//input[@id='company']").send_keys(company)
#
#     time.sleep(.5)
#     driver.find_element(By.XPATH, "//table[@class ='smart-search-entity-hints']").click()
#
#     driver.find_element(By.XPATH, "//button[@id='btnViewAllFilings']").click()
#     time.sleep(.5)
#     driver.find_element(By.XPATH, "//input[@id='filingDateFrom']").clear()
#     driver.find_element(By.XPATH, "//input[@id='filingDateFrom']").send_keys("2000-01-01")
#     time.sleep(.5)
#     driver.find_element(By.XPATH, "//span[normalize-space()='CSV']").click()

