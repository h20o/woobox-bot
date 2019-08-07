import requests
from multiprocessing.dummy import Pool
import random
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
url = 'https://6sides.lt/forumas/topic/234-3-beta/'
def req_split(r):
	ua = UserAgent()
	#requests.head is much faster than requests.get if your intention is only to get the status code
	headers = {
	"User-Agent": ua.random
	}
	for pasw in open('urls.txt', 'r'):
		pasw = pasw.replace('\n', '')
		random_lines = random.choice(open("urls.txt").readlines())
		proxies = {
		"https": random_lines.replace('\n', '')
		}
		try:
			req = requests.get("https://woobox.com/c38i43", headers=headers, proxies=proxies, timeout=30)
			bs = BeautifulSoup(req.content, 'html.parser')
			scriptas = bs.find('script')
			p_data = re.findall(r'(?:"session_name" : ")(.*?)(?:,)', str(scriptas))
			jsonas = json.dumps(p_data)
			data = {
			"appid": "143103275748075",
			"actions": "generate",
			"submitted": "1",
			"ci_session": req.cookies['ci_session'],
			"vote": "1"
			}
			req2 = requests.post("https://woobox.com/c38i43", data=data, cookies=req.cookies, timeout=30, proxies=proxies)
			if req2.status_code == 200:
				print("[*] +1 balsas {}".format(proxies))
		except:
			pass
	if req.status_code == 404:
		print(req.content)
		temp = r #return the url string if the server report OK
	else:
		temp = 0
		return temp

data = range(0,5000)

with Pool(650) as p:
	pm = p.imap_unordered(req_split,data)
	pm = [i for i in pm if i]