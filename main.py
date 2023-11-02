from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
import csv

keyword=input("What do you want to search for?")
indeed=extract_indeed_jobs(keyword)
wwr=extract_wwr_jobs(keyword)
jobs=indeed+wwr

file=open(f"{keyword}.csv","w", newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(["Position","Company","Location","URL"])
for job in jobs.reverse():
    csv_writer.writerow([job["position"],job["company"],job["location"],job["link"]])
file.close()
