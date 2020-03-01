import sqlite3

import pytest
from flaskr.db import get_db

#----------------------------------------------------------------------
# DBの取得・Closeのテスト
#----------------------------------------------------------------------
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

#----------------------------------------------------------------------
# init-dbコマンドでinit_dbが正しく呼ばれるかのテスト
#----------------------------------------------------------------------
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True

    # init_dbが呼ばれるはずのところをfake_init_dbに差し替えている
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
