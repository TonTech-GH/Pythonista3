echo off
rem pipにflaskrを登録し、どのディレクトリからでも実行できるようにする
python -m pip install -e .

echo.
echo.

rem 登録されたか確認
python -m pip list

pause
