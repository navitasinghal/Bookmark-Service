from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/"

req = Request(url, headers={'User-agent': 'Chrome/81.0.4044.92'})
html = urlopen(req).read()
soup = BeautifulSoup(html)

for script in soup(["script", "style"]):
    script.extract()    

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)