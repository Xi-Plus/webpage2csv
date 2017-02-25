def match(content):
	import re
	match = re.findall('<td>(.+?)</td><td>(.+?)</td>', content)
	res = []
	for temp in match:
		res.append([temp[0], temp[1]])
	return res

def next(content):
	match = re.search("<a href='([^']+)' id='next'>Next Page<\/a>", content)
	if match == None:
		return False
	else :
		return match.group(1)
