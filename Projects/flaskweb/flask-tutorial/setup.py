#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# FlaskrをDistributeするためのsetup
#  - pipでのインストール時にこの setup.py が参照される
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
from setuptools import find_packages, setup

#----------------------------------------------------------------------
# Setup
#----------------------------------------------------------------------
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),   # 同梱すべきパッケージディレクトリとPythonファイル群。find_packages()で自動的に洗い出してくれる。
    include_package_data=True,  # 上記以外の同梱すべきファイルがある場合はTrue。MANIFEST.inで詳細を指定する必要がある。
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

