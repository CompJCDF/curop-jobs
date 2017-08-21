import json
import time
import os.path

from requests import get
from datetime import datetime
from bs4 import BeautifulSoup

# create set to get only the unique links
htfpLinks = set()

localtime = datetime.now().strftime("%Y-%b-%d--%H-%M-%S")
print(localtime)


data = []

# the first url to the job links
urls = ["https://www.journalism.co.uk/media-reporter-jobs/s64/"]

# getting all the job links
for url in urls:
    html = get(url).text
    bsObj = BeautifulSoup(html, "html.parser")
    addsDiv = bsObj.find("div", class_="yui-u")
    jobAdds = addsDiv.find_all("div", class_="box")
    for job in jobAdds:
        jobTitle = job.find("span", class_="title")
        jobLink = jobTitle.find("a")
        htfpLinks.add(jobLink.get('href'))

print(htfpLinks)

# download links data
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

    # creating the json object
    html = get(data[row]["link"]).text
    bsObj = BeautifulSoup(html, "html.parser")
    addHeader = bsObj.find('div', class_="headline-post")
    role = addHeader.find('h1').getText().strip()
    try:
        employer = addHeader.find_all('dd')[0].getText().strip()
    except IndexError:
        employer = ""
    try:
        location = addHeader.find_all('dd')[2].getText().strip()
    except IndexError:
        location = ""
    addInfo = bsObj.find('div', class_="post-info")
    postedOn = addInfo.find('span').getText().strip()
    addContent = bsObj.find('div', class_="post-content")
    detailsTags = str(addContent)
    details = addContent.getText().strip()
    data[row]["DetailsTags"] = detailsTags
    data[row]["Details"] = details
    data[row]["Role"] = role
    data[row]["Duplicate"] = 0
    data[row]["Recruiter"] = employer
    data[row]["Location"] = location
    data[row]["PostedOn"] = postedOn
    data[row]["Industries"] = []
    data[row]["Sectors"] = []
    data[row]["Disciplines"] = []

with open('journalism_%s.json' % (localtime), 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4)
