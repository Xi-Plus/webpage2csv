import urllib.request
import csv
from datetime import datetime, timedelta
import importlib

import config as cfg

f = open("output.csv","w")
f.write('\ufeff')
w = csv.writer(f)
for use in cfg.uses:
	print("使用  "+use)
	for website in cfg.websites[use]:
		print("載入模組 "+website["plugin"])
		plugin = importlib.import_module("plugins."+cfg.plugins[website["plugin"]])
			
		url = website["url"]

		while True:
			print("開始抓取網頁 "+url)
			timer = datetime.now()
			req = urllib.request.Request(
					url, 
					data=None, 
					headers={
							'User-Agent': cfg.UserAgent
					}
			)
			web = urllib.request.urlopen(req)
			content = web.read()
			web.close()
			print("抓取網頁花費 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")

			timer = datetime.now()
			content = content.decode(website["charset"], 'ignore')
			print("編碼花費 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")

			timer = datetime.now()
			res = plugin.match(content)
			print("分析花費 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")

			timer = datetime.now()
			for row in res:
				temp = [url]
				temp.extend(row)
				w.writerows([temp])
			print("寫檔花費 "+str(round((datetime.now()-timer).total_seconds()*1000, 2))+" ms")
			url = plugin.next(content)
			if url == False:
				print("沒有下一頁，退出")
				break

f.close()
