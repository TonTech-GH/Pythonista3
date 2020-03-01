echo off
rem DBの初期化。既存のDBは消えるので注意。
set FLASK_APP=flaskr
set FLASK_ENV=development
python -m flask init-db

pause
