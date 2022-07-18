import requests
from bs4 import BeautifulSoup
import re
import math

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  # pagination = soup.find("div",{"class": "pagination"})
  # pages = pagination.find_all('a')
  # spans = []
  # for page in pages :
  #   spans.append(page.find("span"))
  # print(spans[0:-1])

# 마지막 페이지 번호 찾기
  searchCountPages = soup.find("div", id="searchCountPages").text
## "1페이지 결과 1,443건"
  searchCountPages = searchCountPages.split("결과")[-1]
## " 1,443건"
  searchCountPages = re.sub("[^0-9]", "", searchCountPages)
## "1443"
  searchCountPages = int(searchCountPages)
## 1443
  max_page = math.ceil(searchCountPages/50)
  return max_page

def extract_job(html):
  title = html.find("a", {"class":"jcs-JobTitle"}).find("span")["title"]
  company = html.find("span", {"class": "companyName"}).string
  location = html.find("div", {"class": "companyLocation"}).string
  job_id = html.find("a", {"class":"jcs-JobTitle"})["data-jk"]
  return {'title':title, 'company':company, 'location':location, 'link':f"https://kr.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")  
    result = requests.get(f"{URL}&start=(page*{LIMIT})")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class":"job_seen_beacon"})
     
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

# results=soup.find_all("div", {"class": "job~~"})
# for results in results:
#   title=result.find("div", {"class": "title"}).find("a")["title"]
#   print(title)