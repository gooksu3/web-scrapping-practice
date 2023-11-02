from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver


browser=webdriver.Chrome()
base_url="https://kr.indeed.com/jobs?q="
search_term="python"

response=browser.get(f"{base_url}{search_term}")
results=[]
num=1
while True:
    soup=BeautifulSoup(browser.page_source,"html.parser")
    job_list=soup.find("ul",class_="css-zu9cdh")
    jobs=job_list.find_all("li",class_="css-51lfssm")
    jobs=job_list.find_all("li",recursive=False)
    for job in jobs:
        zone=job.find("div",class_="mosaic-zone")
        if zone==None:
            # h2=job.find("h2",class_="jobTitle")
            # a=h2.find("a")
            # anchor=job.select("h2 a") <--list로 반환
            anchor=job.select_one("h2 a")
            title=anchor['aria-label']
            link=anchor['href']
            company=job.find("div",class_="company_location")
            company_name=company.find("span",class_="css-1x7z1ps")
            company_location=company.find("div",class_="css-t4u72d")
            if company_location==None:
                job_data={
                    "link":f"https://kr.indeed.com{link}",
                    "company":company_name.string,
                    "location":"",
                    "position":title
                }
            else:                
                job_data={
                    "link":f"https://kr.indeed.com{link}",
                    "company":company_name.string,
                    "location":company_location.string,
                    "position":title
                }
            print(job_data,"\n//////////////////////////////")
            results.append(job_data)
    nav=soup.find("nav",class_="css-jbuxu0")
    next_arrow=nav.find_all("div")[-1]
    if next_arrow.find("svg")==None:
        break
    else:
        response=browser.get(f"https://kr.indeed.com/jobs?q=python&start={num}0&pp=gQAPAAABi3r6du8AAAACFWpRbAAkAQEBCSC41bUZzlIycTe6nIDULgTnRivNHXKcJxVze1W9kuXzAAA")
        num+=1
print(results)
    


