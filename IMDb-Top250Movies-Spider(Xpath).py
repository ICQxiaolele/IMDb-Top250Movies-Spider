# -*- coding:utf-8 -*-

import requests
import re
import json
import time
import random
from lxml import etree


def get_all_url():
	url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
	}
	try:
		response = requests.get(url=url,headers=headers)
		if response.status_code == 200:
			return response.text
		else:
			print('响应状态码异常-get_all_url')
			return None
	except:
		print('数据获取异常-get_all_url')
		return None

def parse_all_url(response):
	html = etree.HTML(response)
	url = html.xpath('//td[@class="titleColumn"]/a/@href')
	def add_url_prefix(x):
		x = 'https://www.imdb.com' + x
		return x
	# 使用map把获取的链接进行完整拼接
	url = list(map(add_url_prefix,url))
	return url

def get_one_info(url):
	USER_AGENTS = [
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]
	User_Agent = random.choice(USER_AGENTS)
	headers = {
	'User-Agent': User_Agent
	}
	response = requests.get(url=url,headers=headers)
	data = {}
	html = etree.HTML(response.text)
	data['rank'] = results.index(url) + 1
	data['title'] = html.xpath('//h1/text()')[0].strip()
	data['rating'] = html.xpath('//span[@itemprop="ratingValue"]/text()')[0]
	types = html.xpath('//div[@class="subtext"]/a/text()')
	if len(types) == 4:
		data['types'] = types[:3]
	elif len(types) == 3:
		data['types'] = types[:2]
	else:
		data['types'] = types[0]
	data['time'] = html.xpath('//div[@class="subtext"]/time/text()')[0].strip()
	data['released'] = html.xpath('//span[@id="titleYear"]/a/text()')[0]
	data['released_exact'] = html.xpath('//div[@class="subtext"]/a[position()=last()]/text()')[0].strip('\n')
	data['users'] = html.xpath('//span[@class="small"]/text()')[0].replace(',','')
	return data
#以json格式保存数据
def save_all_info(txt):
	with open('result.json','a',encoding='utf-8') as f:
		f.write(json.dumps(txt,ensure_ascii=False) + '\n')

def main():
	result_list = []
	response = get_all_url()
	global results
	results = parse_all_url(response)
	# 循环获取每个电影的详细数据
	for result in results:
		txt =get_one_info(result)
		print(txt)
		save_all_info(txt)

	
if __name__ == '__main__':
	main()
