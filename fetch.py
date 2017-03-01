# -*- coding: utf-8 -*-
import urllib.request
import csv
from datetime import datetime, timedelta
import importlib
import config as cfg

print("可使用的名稱如下")
for website in cfg.websites:
	print("  "+website)
print("輸入要抓取的名稱，以空格隔開：", end="")
try:
	uses = input().split()
except KeyboardInterrupt:
	print()
	print("使用者取消操作")
	exit()

f = open("output.csv", "w", encoding = 'utf8', newline='')
f.write('\ufeff')
w = csv.writer(f)
for use in uses:
	print("使用  "+use)
	try:
		if use not in cfg.websites:
			print("找不到 "+use)
			continue
		for website in cfg.websites[use]:
			print("載入模組 "+website["plugin"])
			plugin = importlib.import_module("plugins."+cfg.plugins[website["plugin"]])
				
			url = website["url"]

			while True:
				print("開始抓取網頁 "+url)
				timer = datetime.now()
				req = urllib.request.Request(
					url, 
					data = None, 
					headers = {
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
	except KeyboardInterrupt:
		print("使用者取消操作")
f.close()
print("已完成匯出")
