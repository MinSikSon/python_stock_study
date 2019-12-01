import urllib.request

def get_html(url):
	# http://pythonstudy.xyz/python/article/19-%ED%81%B4%EB%9E%98%EC%8A%A4
	__html = "" # python private variable need `__`
#response = requests.get(url)
#if response.status_code == 200:
#		html = resp.text
	__html = urllib.request.urlopen(url).read()
	return __html