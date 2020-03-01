# Pythonistaでシェルを使用可能にする
# pipも使えるようになる
import requests as r;
exec(r.get('http://bit.ly/get-stash').text)

print('インストール完了したらPythonistaを再起動する')
