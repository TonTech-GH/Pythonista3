# coding: utf-8
# ==================================
# エクステンションで渡されたファイル、フォルダを複製
# 複製したら名前に '-copy' が付加される
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import os
import editor	# 編集中のファイルパス取得
import shutil	# ファイルコピー
import console	# ダイアログ表示

# ----------------------------------
# 定義
# ----------------------------------
# 複製時の追加文字列
AddStr = '-copy'

# ----------------------------------
# 処理
# ----------------------------------
def main():
	# 編集中のファイルのパスを取得
	fpath = editor.get_path()
	NAME = os.path.basename(fpath)
	PATH = os.path.dirname(fpath)
	
	# エラーチェック
	if os.path.isfile(fpath) != True:
		assert False, NAME + '\n is not file'
		
	# 複製とわかる名前でコピー
	t = NAME.split('.')
	shutil.copyfile(fpath, os.path.join(PATH, t[0] + AddStr + '.' + t[1]))
	
	# ダイアログ表示
	console.alert(NAME + '\nCopied!', '', 'OK', hide_cancel_button=True)

# ----------------------------------
# 単体テスト
# ----------------------------------
if __name__ == '__main__':
	main()
