from robots import Robot, RobotsFile

niz = """User-agent: *
Disallow: /admin
Disallow: /resources
Disallow: /pomoc

User-agent: Googlebot
Disallow: /admin
Disallow: /resources
Disallow: /pomoc

Sitemap: https://www.gov.si/sitemap.xml
"""


print(RobotsFile.razdeli_robots_datoteko(niz)[2])

a = Robot(RobotsFile.razdeli_robots_datoteko(niz)[0])

print(a.disallow)


