import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  #open은 파일을 연다. 해당 파일이 없으면 생성한다.
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return