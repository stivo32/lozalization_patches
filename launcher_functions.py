# coding: utf-8

import requests
import re
import os
import os.path
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


DISTRIBUTION_PARAMS = {
    'sg': {
        'launcher_update_url': 'http://update.worldoftanks.asia',
        'langs': ['fil', 'id', 'ja', 'ko', 'ms', 'th', 'vi', 'zh_sg', 'zh_tw', 'en'],
    },
    'ru': {
        'launcher_update_url': 'http://update.wot.ru.wargaming.net',
        'langs': ['be', 'uk', 'kk', 'ru'],
    },
    'eu': {
        'launcher_update_url': 'http://update.worldoftanks.eu',
        'langs': ['pt', 'de', 'no', 'sr', 'fi', 'es', 'hu', 'pl', 'nl', 'it', 'hr', 'fr', 'lt', 'el', 'da', 'bg',
                  'lv', 'et', 'cs', 'tr', 'sv', 'ro', 'en'],
    },
    'na': {
        'launcher_update_url': 'http://update.worldoftanks.com',
        'langs': ['ja', 'ko', 'pt_br', 'fr', 'es_ar', 'en'],
    },
    'cn': {
        'launcher_update_url': 'http://update.worldoftanks.cn',
        'langs': ['zh_cn'],
    },

}

__all__ = ['get_patches_with_launcher']


def get_patches_with_launcher(realm):
    list_with_urls = get_urls(realm)
    download_patches(realm, list_with_urls)


def get_urls(realm):
    params = dict()
    list_with_urls = list()
    params['protocol_ver'] = '4'
    params['install_id'] = 'C8BD7B9BD74484CC719CE637719CE6370ADF6C3C'
    params['target'] = 'locale'
    params['locale_ver'] = '0'
    for lang in DISTRIBUTION_PARAMS[realm]['langs']:
        params['lang'] = lang
        response = requests.get(DISTRIBUTION_PARAMS[realm]['launcher_update_url'], params=params)
        content = response.content
        pattern = r'<http name="\w*">(.*)</http>'
        url_to_download = re.search(pattern, content)
        list_with_urls.append(url_to_download.group(1))
    print 'Links have been got.'
    return list_with_urls


def download_patches(realm, list_with_urls):
    if not os.path.exists(realm):
        os.mkdir(realm)
    patch_names = list()
    for url in list_with_urls:
        response = requests.get(url)
        patch_name = re.split('/', url)[-1]
        patch_names.append(patch_name)
        if response:
            print '{} has been downloaded'.format(patch_name)
        open(os.path.join(os.getcwd(), realm, patch_name), 'wb').write(response.content)