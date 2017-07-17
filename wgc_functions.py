# coding: utf-8
import os
import os.path
import time
import psutil
import shutil

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

CLIENT_PATHES = 'client.xml'


DISTRIBUTION_PARAMS = {
    'sg': {
        'langs': ['fil', 'id', 'ja', 'ko', 'ms', 'th', 'vi', 'zh_sg', 'zh_tw', 'en'],
    },
    'ru': {
        'langs': ['be', 'uk', 'kk', 'ru'],
    },
    'eu': {
        'langs': ['pt', 'de', 'no', 'sr', 'fi', 'es', 'hu', 'pl', 'nl', 'it', 'hr', 'fr', 'lt', 'el', 'da', 'bg',
                  'lv', 'et', 'cs', 'tr', 'sv', 'ro', 'en'],
    },
    'na': {
        'langs': ['ja', 'ko', 'pt_br', 'fr', 'es_ar', 'en'],
    },
    'cn': {
        'langs': ['zh_cn'],
    },

}

__all__ = ['get_patches_with_wgc']


def get_patches_with_wgc(realm):
    if not os.path.exists(CLIENT_PATHES):
        print 'There is no client.xml with settings'
        raw_input()
        exit()
    path_to_client = get_path(realm)
    path_to_wgc_exe = os.path.join(path_to_client, 'wgc_api.exe')
    path_to_game_info = os.path.join(path_to_client, 'game_info.xml')
    path_to_update_folder = os.path.join(path_to_client, 'Updates')
    if not os.path.exists(path_to_wgc_exe):
        print 'Path "{}" is not exist'.format(path_to_wgc_exe)
        raw_input()
        exit()
    if not os.path.exists(path_to_game_info):
        print 'Path "{}" is not exist'.format(path_to_game_info)
        raw_input()
        exit()
    cleanup_update_folder(path_to_update_folder)
    for lang in DISTRIBUTION_PARAMS[realm]['langs']:
        change_game_info(path_to_game_info, lang)
        loc_rev = get_localization_rev(path_to_game_info)
        os.system(path_to_wgc_exe)
        while loc_rev == '0':
            time.sleep(5)
            loc_rev = get_localization_rev(path_to_game_info)
        for proc in psutil.process_iter():
            if proc.name() == 'wgc.exe':
                proc.kill()
                break
    move_patches(realm, path_to_update_folder)


def get_path(realm):
    def get_tag_text(root, path):
        return root.find('./{}'.format(path)).text.strip()

    try:
        tree = et.ElementTree(file=CLIENT_PATHES)
    except IOError:
        tree = None
    if tree is not None:
        root = tree.getroot()
        path_to_client = get_tag_text(root, realm)
    else:
        path_to_client = None
    return path_to_client


def change_game_info(path_to_game_info, lang):
    try:
        tree = et.ElementTree(file=path_to_game_info)
    except IOError:
        print "Can't read {}".format(path_to_game_info)
        raw_input()
        exit()
    root = tree.getroot()
    localization = root.find('.//localization')
    localization.text = lang.upper()
    version = root.find('.//value[@name="locale"]')
    version.text = '0'
    tree.write(path_to_game_info)


def get_localization_rev(path_to_game_info):
    try:
        tree = et.ElementTree(file=path_to_game_info)
    except IOError:
        print "Can't read {}".format(path_to_game_info)
        raw_input()
        exit()
    root = tree.getroot()
    version = root.find('.//value[@name="locale"]')
    return version.text


def open_wgc(path_to_wgc):
    os.system(path_to_wgc)


def cleanup_update_folder(path_to_update_folder):
    if not raw_input('Need to clean up Updates folder before downloading.'
                 ' Enter Y|y to continue or any other key to exit\n').lower() == 'y':
        raw_input('Please press enter to exit')
        exit()
    list_of_folders = os.listdir(path_to_update_folder)
    for folder in list_of_folders:
        shutil.rmtree(os.path.join(path_to_update_folder, folder))


def move_patches(realm, path_to_update_folder):
    list_of_patch_folders = os.listdir(path_to_update_folder)
    if len(list_of_patch_folders) == 0:
        print 'There are no patch folders. Please check patch downloading.\n'
        raw_input()
        exit()
    elif len(list_of_patch_folders) > 1:
        print 'There are several patch folders. May be there are patches from previous version.'
        raw_input()
        exit()
    path_to_loc_files = os.path.join(path_to_update_folder, list_of_patch_folders[0])
    list_of_files = os.listdir(path_to_loc_files)
    for file in list_of_files:
        if 'locale' in file:
            print 'Copy {} for comparing'.format(file)
            shutil.copy(os.path.join(path_to_loc_files, file), os.path.join(os.getcwd(), os.path.join(realm, file)))


def main():
    get_patches_with_wgc('ru')


if __name__ == '__main__':
    main()