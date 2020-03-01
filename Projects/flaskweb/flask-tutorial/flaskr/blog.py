#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# ブログビュー
#
#======================================================================
#----------------------------------------------------------------------
# import files
#----------------------------------------------------------------------
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

#----------------------------------------------------------------------
# 定義
#----------------------------------------------------------------------
bp = Blueprint('blog', __name__)

#----------------------------------------------------------------------
# メインページ
#----------------------------------------------------------------------
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

#----------------------------------------------------------------------
# 記事投稿
#----------------------------------------------------------------------
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

#----------------------------------------------------------------------
# DBから記事データの取得
#----------------------------------------------------------------------
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        # abort : HTTPステータスを返す特別な例外を発生させる
        # 404 : Not Found
        # 第2引数に文字列指定するとその文字列を表示する。指定無しならばデフォルトメッセージ。
        abort(404, "Post id {0} doesn't exist.".format(id))
    
    if check_author and post['author_id'] != g.user['id']:
        # 403 : Forbidden(閲覧禁止)
        abort(403)

    return post

#----------------------------------------------------------------------
# 記事の更新
#----------------------------------------------------------------------
# 引数 int:id がある。記事を特定するためのIDのこと。int: を無くすとStringとして扱われる。
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # DBの記事データを更新
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

#----------------------------------------------------------------------
# 記事の削除
#----------------------------------------------------------------------
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

