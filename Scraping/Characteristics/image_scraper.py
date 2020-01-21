
from bs4 import BeautifulSoup
import requests

url = "https://www.phosphosite.org/proteinAction?id=570&showAllSites=true"


page = requests.get(url)
print(page)
soup = BeautifulSoup(page.text, "html.parser")
print(page.text)

#
# for start in soup.find_all('img'):
#     print(start, "\n")
