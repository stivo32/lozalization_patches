# coding: utf-8
import requests
import re

def get_urls():

	http_url = 'http://update.worldoftanks.asia'
	params = dict()
	locs = ['en', 'fil', 'id', 'ja', 'ko', 'ms', 'th', 'vi', 'zh_sg', 'zh_tw']
	list_with_urls = list()
	params['protocol_ver'] = '4'
	params['install_id'] = 'CF4D3B3C1C11CC8067F81B6967F81B690E861BBE'
	params['target'] = 'locale'
	params['locale_ver'] = '0'
	params['lang'] = 'en'
	for loc in locs:
		params['lang'] = loc
		response = requests.get(http_url, params=params)
		content = response.content
		pattern = r'<http name="\w*">(.*)</http>'
		url_to_donwload = re.search(pattern, content)
		list_with_urls.append(url_to_donwload.group(1))
	return list_with_urls


def download_patches(list_with_urls):
	for url in list_with_urls:
		response = requests.get(url)
		patch_name = re.split('/', url)[-1]
		with open(patch_name, 'wb') as patch:
			patch.write(response.content)


def compare_patches():
	pass


def main():
	urls = get_urls()
	download_patches(urls)

if __name__ == '__main__':
	main()