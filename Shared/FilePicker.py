# ==================================
# ファイルアプリのファイルから選択してコピー
# ==================================
# ----------------------------------
# import module
# ----------------------------------
# OSのダイアログ表示
# ファイルアプリでアクセスできるファイルのパス取得機能もある
import dialogs	

import os.path
from FileManager import CopyFile as cp

# ----------------------------------
# 定義
# ----------------------------------
DPRINT = False #__name__ == '__main__'
def dp(s):
	if DPRINT:
		print(s)

# --------------------------------
# ファイル取得
# --------------------------------
def PickFilePath():
	fPath = dialogs.pick_document()
	dp(fPath)
	return fPath
	
# --------------------------------
# ファイルコピー
# --------------------------------
def CopyToCur(fPath):
	# ファイル名
	fName = os.path.basename(fPath)
	dp('File Name: ' + fName)
	
	cp(fPath, fName)

# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	fPath = PickFilePath()
	if fPath != None:
		CopyToCur(fPath)

