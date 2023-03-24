from robots import Robot, RobotsFile
from vmesnik import *
from baza import *

niz = """User-agent: *
Disallow: /admin
Disallow: /resources
Disallow: /pomoc

User-agent: Googlebot
Disallow: /admin
Disallow: /resources
Disallow: /pomoc

Sitemap: https://www.gov.si/sitemap.xml
http://gov.si/",
                    "http://evem.gov.si/",
                    "http://e-uprava.gov.si/",
                    "http://e-prostor.gov.si/"
"""
vmesnik1 = Vmesnik()

r = RobotsFile('http://evem.gov.si',None,vmesnik1)
# r = RobotsFile('https://e-uprava.gov.si',None,vmesnik1)
print(r.sitemap.vsebina)

# a=r.robot
# print(a.user_agent)
# import requests
# a = requests.get('http://e-uprava.gov.si/robots.txt', timeout=(3, 30))
# print(a.text)

# print(r.vsebina)
# a = Robot(RobotsFile.razdeli_robots_datoteko(niz)[0])
# print(a)



# print(a.disallow)


