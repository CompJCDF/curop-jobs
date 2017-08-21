import json
import time
import math
import os.path

from requests import get
from datetime import datetime
from bs4 import BeautifulSoup

localtime = datetime.now().strftime("%Y-%b-%d--%H-%M-%S")
print(localtime)

# create set to get only the unique links
htfpLinks = set()

data = []

totalNumberOfAds = 0
urls = ["http://www.gorkanajobs.co.uk/jobs/journalist/"]
for url in urls:
    html = get(url).text
    bsObj = BeautifulSoup(html, "html.parser")
    numberOfJobs = str(bsObj.find("h2"))
    totalNumberOfAds = int(numberOfJobs.split()[1])

pages = totalNumberOfAds / 40
if totalNumberOfAds % 40 != 0:
    pages += 1

for url in urls:
    for page in range(1, int(pages) + 1):
        newUrl = url + str(page) + "/"
        html = get(newUrl).text
        bsObj = BeautifulSoup(html, "html.parser")

        jobList = bsObj.find(id="listing")

        jobAdds = jobList.find_all("li", class_="lister__item")

        for job in jobAdds:
            jobTitle = job.find('h3')
            jobLink = jobTitle.find('a')
            htfpLinks.add(jobLink.get('href'))

print(htfpLinks)

for row1, link in enumerate(htfpLinks):
    #checks if this link exist
    flag = False
    for entry in data:
        if entry["link"] == "http://www.gorkanajobs.co.uk" + link:
            flag = True
            break
    if flag == True:
        break;

    #if the link does not exist we will add it to the list
    data.append({'link': "http://www.gorkanajobs.co.uk" + link})

    #sleep to not overload the servers and printing the current page processed
    time.sleep(1)
    print(row1)

    html = get(data[row1]["link"]).text
    bsObj = BeautifulSoup(html, "html.parser")
    details = bsObj.find(itemprop="description")
    title = bsObj.find(itemprop="title").getText().strip()
    data[row1]["DetailsTags"] = str(details)
    data[row1]["Details"] = details.getText()
    data[row1]["Role"] = title
    data[row1]["Duplicate"] = 0
    table = bsObj.find_all("div", class_="cf margin-bottom-5")
    for row in table:
        info = row.find('dt').getText().strip()
        if info == "Recruiter":
            recruiter = row.find(itemprop="name").getText().strip()
            data[row1]["Recruiter"] = recruiter
        if info == "Location":
            location = row.find('dd').getText().strip()
            data[row1]["Location"] = location
        if info == "Posted":
            postedOn = row.find(itemprop="datePosted").getText().strip()
            data[row1]["PostedOn"] = postedOn
        if info == "Industry":
            industries = row.find_all('a')
            data[row1]["Industries"] = []
            for industry in industries:
                data[row1]["Industries"].append({'Industry': industry.getText().strip()})
        if info == "Sector":
            sectors = row.find_all('a')
            data[row1]["Sectors"] = []
            for sector in sectors:
                data[row1]["Sectors"].append({'Sector': sector.getText().strip()})
        if info == "Discipline":
            disciplines = row.find_all('a')
            data[row1]["Disciplines"] = []
            for discipline in disciplines:
                data[row1]["Disciplines"].append({'Discipline': discipline.getText().strip()})

with open('gorkana_%s.json' % (localtime), 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4)
