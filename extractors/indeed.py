from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver

browser=webdriver.Chrome()

def get_page_count(keyword):
    base_url="https://kr.indeed.com/jobs?q="
    response=browser.get(f"{base_url}{keyword}")
    soup=BeautifulSoup(browser.page_source,"html.parser")
    pagination=soup.find("nav",class_="css-jbuxu0")
    if pagination==None:
        return 1
    else:
        pages=pagination.find_all("div",recursive=False)
        count=len(pages)
        if count>=5:
            return 5
        else:
            return count


def extract_indeed_jobs(keyword):
    results=[]
    pages=get_page_count(keyword)
    print("Found",pages, "pages")
    for page in range(pages):
        base_url="https://kr.indeed.com/jobs?q="
        final_url=f"{base_url}{keyword}&start={page*10}"
        response=browser.get(final_url)
        print("Requesting", final_url)
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
                job_data={
                    "link":f"https://kr.indeed.com{link}",
                    "company":company_name.string,
                    "location":company_location.string,
                    "position":title
                }
                results.append(job_data)
    return results