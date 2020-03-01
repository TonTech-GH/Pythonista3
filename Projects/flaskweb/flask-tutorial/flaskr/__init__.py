#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Flaskのアプリケーションファクトリー
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
import os
from flask import Flask # Webアプリ用マイクロフレームワーク

#----------------------------------------------------------------------
# アプリケーションファクトリー関数
#----------------------------------------------------------------------
def create_app(test_config=None):
    # アプリインスタンスの生成
    #  - __name__ : アプリがいくつかのパスを設定するためにどこで実行されているかを伝える必要がある
    #  - instance_relative_config : 設定ファイルがインスタンスフォルダに関連付けられていることをアプリに伝えている
    #    インスタンスフォルダはflaskrパッケージの外側に位置し、設定シークレットやデータベースファイルなどのローカルデータが置かれる
    app = Flask(__name__, instance_relative_config=True)

    # デフォルトの設定
    app.config.from_mapping(
        SECRET_KEY='dev',   # データを安全に保存するために使われる。本番デプロイ時はランダム値に変更すべき。
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # SQLiteデータベースファイルの保存先パス
    )

    if test_config is None:
        # テストじゃないときは設定ファイルの読み込み(デフォルト設定を上書き)
        # ※インスタンスフォルダに存在するときのみ
        app.config.from_pyfile('config.py', silent=True)
    else:
        # テスト用設定の読み込み
        app.config.from_mapping(test_config)

    # インスタンス用フォルダーが存在するか確認
    # Flaskはインスタンスフォルダを自動で作らないため作ってあげる必要がある
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # DBの初期化
    from . import db
    db.init_app(app)

    # 認証ビューの登録
    from . import auth
    app.register_blueprint(auth.bp)

    # ブログビューの登録
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

