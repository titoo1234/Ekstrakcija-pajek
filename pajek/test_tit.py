from urllib.parse import urljoin, urlparse

import vmesnik
SEEDs = [
            "http://gov.si/",
                    "http://evem.gov.si/",
                    "http://e-uprava.gov.si/",
                    "http://e-prostor.gov.si/"
                    ]

# for i in range(3):
#     link = SEEDs[i]
#     domena = urlparse(link).netloc
#     print(domena)
# link = SEEDs[0]
# vm = vmesnik.Vmesnik()
# vm.nastavi_stran(link)
# slike = vm.poisci_slike()
# for i in slike:
#     print(i)
# print(len(slike))
import binascii
from PIL import Image
import requests
from io import BytesIO
url = 'https://www.gov.si/assets/vladne-sluzbe/UKOM/gov-si/Fotografije/sodeluj/GettyImages-166000471-republica__FillWzQ0MCwyOTIsImE1MjU3MmM1MTYiXQ.jpg'
response = requests.get(url)
img = Image.open(BytesIO(response.content))



content = img.read()
print(binascii.hexlify(content))
print(img.getdata())


# Image.open(urlopen(url))
# with open(filename, 'rb') as f:
#     content = f.read()
# print(binascii.hexlify(content))
