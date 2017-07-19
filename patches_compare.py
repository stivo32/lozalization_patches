# coding: utf-8

import os.path
import os
import shutil
from wgc_functions import *
from launcher_functions import *


def compare_patches(realm):
    flag = True
    reference_dir = '{}_reference'.format(realm)
    print 'Patches comparing...'
    reference_path = os.path.join(os.getcwd(), reference_dir)
    downloaded_path = os.path.join(os.getcwd(), realm)
    reference_patches = os.listdir(reference_dir)
    downloaded_patches = os.listdir(realm)
    if not reference_patches == downloaded_patches:
        raise Exception('List of downloaded patches is different with reference')
    for patch in downloaded_patches:
        if not open(os.path.join(reference_path, patch)).read() == open(os.path.join(downloaded_path, patch)).read():
            flag = False
            print 'Downloaded patch {} is not the same with reference'.format(patch)
    if flag:
        print 'Patches are same with references'


def main():
    while True:
        distribution = raw_input('Enter 1 for launcher, 2 for wgc and 0 for exit\n')
        if distribution == '0':
            exit()
        if distribution in ['1', '2']:
            break

    while True:
        realm = raw_input('Enter region: ru, eu, na, sg{} or 0 to exit\n'.format(', cn' if distribution == '1' else ''))
        if distribution == '1' and realm in ['ru', 'eu', 'na', 'sg', 'cn']:
            break
        elif distribution == '2' and realm in ['ru', 'eu', 'na', 'sg']:
            break
        elif realm == '0':
            exit()
    if os.path.exists(realm):
        shutil.rmtree(realm)
    os.mkdir(realm)
    if distribution == '1':
        get_patches_with_launcher(realm)
    else:
        get_patches_with_wgc(realm)

    compare_patches(realm)


if __name__ == '__main__':
    main()
