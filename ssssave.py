from bs4 import BeautifulSoup
import urllib
import hashlib

def download_images_ffffound_pag(urlString, download_location):	
	url = urllib.urlopen(urlString)
	markup = url.read()
	url.close()
	new_soup = BeautifulSoup(markup,"lxml")
	urlsImagenes = new_soup.select(".description")
	for url in urlsImagenes:
		url_image = url.contents[0]		
		if len(url_image)<255:
			local_path = 	download_location+url_image.replace("/",":")
		else:
			local_path = 	download_location+url_image.replace("/",":")[:250]	
		print "saving " + url_image + " in "+ local_path
		urllib.urlretrieve("http://" + url_image, local_path)			 

url_found = "http://ffffound.com/home/paco/found/"
download_location = "/Volumes/Datos HD/ffffound/"

f = urllib.urlopen(url_found)
s = f.read()
f.close()

soup = BeautifulSoup(s,"lxml")

paginas = soup.select("span.paging a[href]")
elems= []

for pagina in paginas:	
	if pagina["href"]:
		if pagina["href"].find("javascript")!=-1:
			elems = pagina["href"].split(",")

pages = int(elems[2])
elems_per_page = int(elems[3])

for i in range(0,pages+1):
	new_url = url_found + "?offset="+str(i*elems_per_page)+"&"
	download_images_ffffound_pag(new_url,download_location)
