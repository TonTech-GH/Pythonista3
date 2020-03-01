#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# 認証関連ビュー
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

#----------------------------------------------------------------------
# 定義
#----------------------------------------------------------------------
# authという名前の設計図を生成
#  url_prefix : このBlueprintに紐づくすべてのURLに付加される
bp = Blueprint('auth', __name__, url_prefix='/auth')


#----------------------------------------------------------------------
# 登録ビュー
#----------------------------------------------------------------------
# /register のURLとregister()関数の紐付け
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # POSTされたフォームの値をキーで取り出し（dict）
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # ちゃんと入力されているか確認
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            # DBに新規登録
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            # 反映
            db.commit()

            # ログインページにリダイレクト
            return redirect(url_for('auth.login'))

        # エラーメッセージの表示
        flash(error)
        
    # 登録ページの表示
    return render_template('auth/register.html')

#----------------------------------------------------------------------
# ログインビュー
#----------------------------------------------------------------------
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # userテーブルからユーザー名が合致するレコードを取り出し
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # バリデーション
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        # 正常ならインデックスページにリダイレクト
        if error is None:
            # リクエストを横断して受け渡せるdictにユーザーIDを登録(cookieに保存される)
            # Flaskによって署名された状態でブラウザに渡されるので改ざんできない
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        # エラーメッセージの表示
        flash(error)

    return render_template('auth/login.html')

#----------------------------------------------------------------------
# ログインしたユーザーデータのロード
#----------------------------------------------------------------------
# このblueprintのすべてのビュー(生成)関数の前に実行される関数を登録
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#----------------------------------------------------------------------
# ログアウト
#----------------------------------------------------------------------
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#----------------------------------------------------------------------
# ビューでのログイン状態確認デコレータ
#----------------------------------------------------------------------
# @login_required を付けた関数はこの関数でラップされる
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # 未ログインならログインページに飛ばす
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
