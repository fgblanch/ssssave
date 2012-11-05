from bs4 import BeautifulSoup
import urllib
import urlparse
import Queue
import threading
import hashlib

def download_images_ffffound_pag(urlString, download_location):	
		url = urllib.urlopen(urlString)
		markup = url.read()
		url.close()
		new_soup = BeautifulSoup(markup,"lxml")
		blocks = new_soup.select("blockquote")

		for block in blocks:
			ffffound_copy_url = block.select("img")[0]["src"]			
			original_image_url = "http://" + block.select(".description")[0].contents[0]
			filename = hashlib.md5(original_image_url).hexdigest() + ffffound_copy_url[(len(ffffound_copy_url)-4):]
			local_path = 	download_location+filename			
			print "saving " + original_image_url + " in "+ local_path
			try:
				result = urllib.urlretrieve(original_image_url, local_path)
				content_type = result[1].getheader("Content-Type")
				if not(content_type) or not (content_type[:5] == 'image'):
					urllib.urlretrieve(ffffound_copy_url, local_path)
			except (IOError):
				pass

class FfffoundPageDownloader (threading.Thread) :	

	def run (self):
		while not pagesQueue.empty():
			new_url = pagesQueue.get()
			download_images_ffffound_pag(new_url,download_location)


url_found = "http://ffffound.com/home/paco/found/"
download_location = "/Volumes/Datos HD/ffffound/"
pagesQueue = Queue.Queue()
threads = 10

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
	pagesQueue.put(new_url)

for x in xrange (threads):
   FfffoundPageDownloader().start()

