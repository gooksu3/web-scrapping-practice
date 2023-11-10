import csv

def save_to_file(file_name,jobs):
    file=open(f"{file_name}.csv","w", newline='',encoding="utf-8")
    csv_writer=csv.writer(file)
    csv_writer.writerow(["Position","Company","Location","URL"])
    for job in jobs:
        csv_writer.writerow([job["position"],job["company"],job["location"],job["link"]])
    file.close()