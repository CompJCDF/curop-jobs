import json
import os.path
import time

from requests import get
from datetime import datetime
from bs4 import BeautifulSoup

localtime = datetime.now().strftime("%Y-%b-%d--%H-%M-%S")
print(localtime)

# create set to get only the unique links
htfpLinks = set()

data = []

urls = ["http://www.holdthefrontpage.co.uk/jobsboard/category/trainee-junior-reporters/", "http://www.holdthefrontpage.co.uk/jobsboard/category/senior-reporters/", "http://www.holdthefrontpage.co.uk/jobsboard/category/specialist-reporters/", "http://www.holdthefrontpage.co.uk/jobsboard/category/online-journalists/", "http://www.holdthefrontpage.co.uk/jobsboard/category/jobs-in-sport/", "http://www.holdthefrontpage.co.uk/jobsboard/category/jobs-in-features/", "http://www.holdthefrontpage.co.uk/jobsboard/category/sub-editing-roles/", "http://www.holdthefrontpage.co.uk/jobsboard/category/jobs-in-photographic/", "http://www.holdthefrontpage.co.uk/jobsboard/category/newsdesk-roles/", "http://www.holdthefrontpage.co.uk/jobsboard/category/management-roles/", "http://www.holdthefrontpage.co.uk/jobsboard/category/broadcast-reporting-roles/", "http://www.holdthefrontpage.co.uk/jobsboard/category/pr-comms-roles/", "http://www.holdthefrontpage.co.uk/jobsboard/category/pr-account-executives/", "http://www.holdthefrontpage.co.uk/jobsboard/category/lecturers/", "http://www.holdthefrontpage.co.uk/jobsboard/category/multimedia-journalists/", "http://www.holdthefrontpage.co.uk/jobsboard/category/other-jobs/"]
for url in urls:
    html = get(url).text
    bsObj = BeautifulSoup(html, "html.parser")

    jobTable = bsObj.find(id="wpjb-job-list")

    tableBody = jobTable.find('tbody')

    jobLinks = tableBody.find_all('a')

    for link in jobLinks:
        htfpLinks.add(link.get('href'))

for row, link in enumerate(htfpLinks):
    #checks if this link exist
    flag = False
    for entry in data:
        if entry["link"] == link:
            flag = True
            break
    if flag == True:
        break;

    #if the link does not exist we will add it to the list
    data.append({'link':link})

    #sleep to not overload the servers and printing the current page processed
    time.sleep(1)
    print(row)

    html = get(data[row]["link"]).text
    bsObj = BeautifulSoup(html, "html.parser")
    addContent = bsObj.find(id="job-content")
    role = addContent.find('h1').getText().strip()
    addHeader = addContent.find("table", class_="wpjb-main-info")
    location = addHeader.find_all('h2')[1].getText().strip()[7:]
    postedOn = addHeader.find_all('td')[2].getText().strip()[8:]
    addInfo = addContent.find("table", class_="wpjb-job-info")
    employer = addInfo.find(itemprop="name").getText().strip()
    industries = addInfo.find_all(itemprop="occupationalCategory")
    sector = addInfo.find_all('td')[len(addInfo.find_all('td')) - 1].getText().strip()
    detailsTags = str(addContent.find("div", class_="wpjb-job-content"))
    details = addContent.find("div", class_="wpjb-job-content").getText().strip()
    data[row]["DetailsTags"] = detailsTags
    data[row]["Details"] = details
    data[row]["Role"] = role
    data[row]["Duplicate"] = 0
    data[row]["Recruiter"] = employer
    data[row]["Location"] = location
    data[row]["PostedOn"] = postedOn
    data[row]["Industries"] = []
    for industry in industries:
        data[row]["Industries"].append({'Industry': industry.getText().strip()})
    data[row]["Sectors"] = []
    data[row]["Sectors"].append({'Sector': sector})
    data[row]["Disciplines"] = []

with open('htfp_%s.json' % (localtime), 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4)
