import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import spacy

options = ChromeOptions()
#options.add_argument("--headless")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5829.0 Safari/537.36')

# Use ChromeDriverManager to automatically download and install the appropriate ChromeDriver
#webdriver_path = ChromeDriverManager().install()
#browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

chrome_driver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
response = requests.get(chrome_driver_version_url)
latest_version = response.text.strip()

webdriver_path = ChromeDriverManager(version=latest_version).install()

# Create the WebDriver instance
browser = webdriver.Chrome(options=options)

print('\n\n\n', "------------- PROFILE FETCHER v1 -------------\n")

jobTitle = input("[*] Enter Job Title: ")
location = input("[*] Enter Location: ")

time.sleep(1)

url = f"http://www.google.com/search?q=+%22{jobTitle}%22+%22{location}%22 -intitle:%22profiles%22 -inurl:%22dir/%22 +site:in.linkedin.com/in/ OR site:in.linkedin.com/pub/&num=1000"

# add'+%22Cybersecurity%22' to the above link to check whether the logic of checking if a company is a cybersecurity company or not working. 

#"CEO" "Delhi" -intitle:"profiles" -inurl:"dir/"  site:in.linkedin.com/in/ OR site:in.linkedin.com/pub/

# First level: div class="MjjYud"
# Second level: div class="g Ww4FFb vt6azd tF2Cxc asEBEc"
# Third level: div class="kvH3mc BToiNc UK95Uc"
# Fourth level: div class="Z26q7c UK95Uc jGGQ5e"
# Fifth level: div class="yuRUbf"
# Sixth level: anchor tag <a>

time.sleep(10)

browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')
divs = soup.find_all('div', {'class': 'MjjYud'})

time.sleep(2)

print("Count: " + str(len(divs)))

time.sleep(1)

links = []
bios = []
cyberchecks = []
names = []
company_name = []

for div in divs:
    try:
        second_div = div.find('div', {'class': 'g Ww4FFb vt6azd tF2Cxc asEBEc'})
        third_div = second_div.find('div', {'class': 'kvH3mc BToiNc UK95Uc'})
        fourth_div = third_div.find('div', {'class': 'Z26q7c UK95Uc jGGQ5e'})
        fifth_div = fourth_div.find('div', {'class': 'yuRUbf'})
        link = fifth_div.find('a')['href']
        links.append(link)
    except Exception as e:
        print(f"An error occurred while processing: {str(e)}")

for newdiv in divs:
    try:
        newsecond_div = newdiv.find('div', {'class': 'g Ww4FFb vt6azd tF2Cxc asEBEc'})
        newthird_div = newsecond_div.find('div', {'class': 'kvH3mc BToiNc UK95Uc'})
        newfourth_div = newthird_div.find('div', {'class': 'Z26q7c UK95Uc'})
        newfifth_div = newfourth_div.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})
        newbio = newfifth_div.find('span')
        bios.append(newbio.text)
    except Exception as e:
        print(f"An error occurred while processing: {str(e)}")
        
#read from a HTML file which has all the keywords
def read_keywords_from_html(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    keyword_list = []

    keyword_elements = soup.find_all('li')
    for keyword_element in keyword_elements:
        keyword_list.append(keyword_element.text.strip())

    return keyword_list

def find_CyberSecurity(some_string):
    keywords = read_keywords_from_html(f"keywords.html")
    return any(keyword in some_string for keyword in keywords)

for newdiv in divs:
    try:
        newsecond_div = newdiv.find('div', {'class': 'g Ww4FFb vt6azd tF2Cxc asEBEc'})
        newthird_div = newsecond_div.find('div', {'class': 'kvH3mc BToiNc UK95Uc'})
        newfourth_div = newthird_div.find('div', {'class': 'Z26q7c UK95Uc'})
        newfifth_div = newfourth_div.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})
        newcybercheck = newfifth_div.find('span')
        if find_CyberSecurity(newcybercheck.text.lower()) == False:
            cyberchecks.append('N')
        else:
            cyberchecks.append('Y')
    except Exception as e:
        print(f"An error occurred while processing the div: {str(e)}")


for newdiv in divs:
    try:
        newsecond_div = newdiv.find('div', {'class': 'g Ww4FFb vt6azd tF2Cxc asEBEc'})
        newthird_div = newsecond_div.find('div', {'class': 'kvH3mc BToiNc UK95Uc'})
        newfourth_div = newthird_div.find('div', {'class': 'Z26q7c UK95Uc jGGQ5e'})
        newfifth_div = newfourth_div.find('div', {'class': 'yuRUbf'})
        newsixth_div = newfifth_div.find('h3', class_='LC20lb MBeuO DKV0Md')
        newname = newsixth_div.text.strip().split(' - ')[0]
        names.append(newname)
    except Exception as e:
        print(f"An error occurred while processing: {str(e)}")

nlp = spacy.load("en_core_web_sm")

def extract_company_names(text):
    doc = nlp(text)
    company_names = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            company_names.append(ent.text)

    return company_names

for newdiv in divs:
    try:
        newsecond_div = newdiv.find('div', {'class': 'g Ww4FFb vt6azd tF2Cxc asEBEc'})
        newthird_div = newsecond_div.find('div', {'class': 'kvH3mc BToiNc UK95Uc'})
        newfourth_div = newthird_div.find('div', {'class': 'Z26q7c UK95Uc'})
        newfifth_div = newfourth_div.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})
        newcompanyname = newfifth_div.find('span')
        companyname = extract_company_names(newcompanyname.text)
        company_name.append(', '.join(companyname))
    except Exception as e:
        print(f"An error occurred while processing the div: {str(e)}")

filename = f"profiles_{jobTitle}_{location}.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Links", "Names", "Bio", "Company Name", "CyberSecurity(Y/N)"])
    for link, name, bio, company_name, cybercheck in zip(links, names, bios, company_name, cyberchecks):
        writer.writerow([link, name, bio, company_name, cybercheck])

print(f"[+] Links saved to '{filename}' file.")
