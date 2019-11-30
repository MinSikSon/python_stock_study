import urllib.request

def get_html(url):
	html = ""
#response = requests.get(url)
#if response.status_code == 200:
#		html = resp.text
	html = urllib.request.urlopen(url).read()
	return html