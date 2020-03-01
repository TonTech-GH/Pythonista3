#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Flaskrのテスト
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

#----------------------------------------------------------------------
# 定義
#----------------------------------------------------------------------
# SQLファイルの読み込み
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
@pytest.fixture
def app():
    # 一時ファイルを作成・オープンし fileオブジェクトとパスを返す
    db_fd, db_path = tempfile.mkstemp()

    # テスト用設定を食わせてアプリケーション生成
    app = create_app({
        'TESTING' : True,       # これを指定するとFlaskがテストモードになる
        'DATABASE': db_path,    # 一時ディレクトリをDBとする
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    # この時点での戻り値を返し、関数を一時的に実行停止させる
    yield app

    os.close(db_fd)
    os.unlink(db_path)

#----------------------------------------------------------------------
# テスト用クライアント
#  - サーバー無しでアプリにリクエストを送るためのクライアントとして使われる
#----------------------------------------------------------------------
@pytest.fixture
def client(app):
    return app.test_client()

#----------------------------------------------------------------------
# テストでClickコマンドを呼ぶためのランナーを生成
#----------------------------------------------------------------------
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

#----------------------------------------------------------------------
# 認証のテスト用アクション
#----------------------------------------------------------------------
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username' : username, 'password' : password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
