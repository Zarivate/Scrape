import scrapy
import json

# This spider handles scraping data from pages where data is displayed through Javascript, meaning it's not static. This example
# only works for sites that utilize XHR, XML http Requests, and bypasses the use of Selenium or Splash to open the page first.
# Instead, direct calls are made to the endpoints in the requests themselves to retrieve the data.

# It's normally easy to tell at a glance from a page's Network tab whether data is rendered dynamically or statically but another way to be
# sure is to click, "disable cache" at the top and then do "Ctrl" + "Shift" + "P", and type in "disable Javascript", then reload the page
# and if nothing or short of nothing is displayed then you can know for certain Javascript is used to render the page.
class JavascriptSpider(scrapy.Spider):
    name = "jsSpider"
    start_urls = ["https://directory.ntschools.net/#/schools"]
    
    # Because the request are JSON requests, headers are needed and thus these dummy ones are used.
    headers = {
            "Accept": "application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.8",
            "Referer":"https://directory.ntschools.net/",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-origin",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "X-Requested-With": "Fetch",
        }
    
    def parse(self, response):
        start_url = "https://directory.ntschools.net/api/System/GetAllSchools"

        yield scrapy.Request(start_url, callback=self.parse_school_api, headers=self.headers)


    # Because a JSON request is going to be processed, CSS or Xpath selectors won't be used like they have in the spiders before this 
    def parse_school_api(self, response):
        # Create the base string that holds the followup API url
        followup_url = "https://directory.ntschools.net/api/System/GetSchool?itSchoolCode="
        # Create a JSON object to hold the data
        data = json.loads(response.body)

        # Because the returned JSON data is in a list format, a for loop is used to iterate through it's data
        for school in data:
            # Grab school id
            school_code = school["itSchoolCode"]
            new_url = followup_url + school_code
            yield scrapy.Request(new_url, callback=self.parse_individual_school, headers=self.headers)

# An example of how the data would look like that the function above handles
# [
#   {
#     "schoolName": "Acacia Hill School",
#     "schoolType": "Specialist School",
#     "electorate": "Braitling",
#     "decsRegion": "Central",
#     "isGovernment": true,
#     "itSchoolCode": "acacisch",
#     "isPreSchool": false
#   },
#   {
#     "schoolName": "Adelaide River School",
#     "schoolType": "Small School",
#     "electorate": "Daly",
#     "decsRegion": "Top End",
#     "isGovernment": true,
#     "itSchoolCode": "adelasch",
#     "isPreSchool": false
#   },
# ]

    
    # Function that handles follow/final API call to get each school's specific data
    def parse_individual_school(self, response):
        # Create a JSON object to hold the data again
        data = json.loads(response.body)
        yield {
            "Name": data["name"],
            "Physical Address": data["physicalAddress"]["displayAddress"],
            "Postal Address": data["postalAddress"]["displayAddress"],
            "Email": data["mail"],
            "Phone Number": data["telephoneNumber"]
        }

       
# An example of how the data would look like that the function above handles        
# {
#   "name": "Angurugu Pre School",
#   "notes": null,
#   "physicalAddress": {
#     "description": "N/A",
#     "state": "NT",
#     "postCode": "Angurugu",
#     "displayAddress": "N/A, Angurugu, NT"
#   },
#   "postalAddress": {
#     "description": null,
#     "state": null,
#     "postCode": ", ",
#     "displayAddress": ", , , "
#   },
# "dn": "ou=Angurugu Pre School,ou=Angurugu School,ou=Government,ou=NTSchools,ou=DEET,dc=nt,dc=gov,c=au",
#   "aliases": [],
#   "region": "East Arnhem",
#   "ntgGeographicDefinition": null,
#   "enrolment": null,
#   "enrolmentDataSource": "2021 Census - 1st week August",
#   "description": null,
#   "religion": null,
#   "hasImage": false,
#   "preSchool": false,
#   "faftSchool": false,
#   "primarySchool": false,
#   "middleSchool": false,
#   "seniorSchool": false,
#   "telephoneNumber": "(08) 89876255",
#   "businessCategories": [
#     "Preschool"
#   ],
#   "ntgGazettedRegion": null,
#   "directorate": null,
#   "schoolElectorate": "Arnhem",
#   "facsimileTelephoneNumber": "(08) 8987 6106",
#   "councilMail": null,
#   "remoteDefinition": null,
#   "long": null,
#   "lat": null,
#   "uri": null,
#   "mail": null,
#   "preSchoolInfo": null,
#   "schoolManagement": []
# }
    

        