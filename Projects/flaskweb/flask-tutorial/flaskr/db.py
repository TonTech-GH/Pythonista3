#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# SQLiteによるデータベース制御
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
import sqlite3

import click
from flask import current_app   # リクエストをハンドリングするためのFlaskアプリを指すオブジェクト
from flask import g             # リクエスト毎のユニークなオブジェクト
from flask.cli import with_appcontext

#----------------------------------------------------------------------
# DBのテーブル生成
#----------------------------------------------------------------------
def init_db():
    # DBに接続
    db = get_db()

    # テーブル生成用SQLスクリプトを読み込んで実行
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# コマンドラインから init-db することで関数を呼び出せるようにしている
@click.command('init-db')
# Flaskのappコンテキストが生成されていない状態で勝手に呼ばれないようにしている
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables. """
    init_db()
    click.echo('Initialized the database.')

#----------------------------------------------------------------------
# DBのコネクション取得
#----------------------------------------------------------------------
def get_db():
    # 同一リクエスト中は1回だけDBに接続され、それを使い回す
    if 'db' not in g:
        # DBに接続
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # 行（レコード）の取得（dictのように使える）
        g.db.row_factory = sqlite3.Row

    return g.db

#----------------------------------------------------------------------
# DBのコネクションを閉じる
#----------------------------------------------------------------------
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#----------------------------------------------------------------------
# アプリの初期化
#----------------------------------------------------------------------
def init_app(app):
    # レスポンスを返した後に実行される関数を登録
    app.teardown_appcontext(close_db)

    # flaskコマンドと一緒に呼ばれうる新コマンドを追加
    app.cli.add_command(init_db_command)
