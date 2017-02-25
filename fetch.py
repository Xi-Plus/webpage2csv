from urllib.request import urlopen
import re
import csv
from datetime import datetime, timedelta
import importlib

import config as cfg

f = open("output.csv","w")
f.write('\ufeff')
w = csv.writer(f)
for use in cfg.uses:
	print("use  "+use)
	for website in cfg.websites[use]:
		print("  website  "+website["url"])

		timer = datetime.now()
		html = urlopen(website["url"])
		content = html.read()
		html.close()
		print("抓取網頁 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")
		timer = datetime.now()
		content = content.decode(website["charset"], 'ignore')
		print("編碼 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")

		plugin = importlib.import_module("plugins."+cfg.plugins[website["plugin"]])
		res = plugin.match(content)

		timer = datetime.now()
		for temp in res:
			w.writerows([[use, website["url"], temp[0], temp[1], temp[2]]])
		print("寫檔 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")

f.close()
