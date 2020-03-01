# ==================================
# ZIPファイルの展開 : パスワード対応版
# 同一ディレクトリの .zip ファイルをすべて展開
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import zipfileSJIS
import os.path 	# ファイル制御
import glob		# ファイル一覧取得

# ----------------------------------
# 定義
# ----------------------------------
# パスワード
PWD = bytes(b'PasswordForUnzip')

# 展開先のディレクトリ名
DST_DIR = 'unzip'

# ----------------------------------
# ZIPファイル展開
# ----------------------------------
def Unzip(fpath):
	if os.path.exists(fpath) == False:
		assert False, fpath + ' is not exist'
		return 
	
	if os.path.exists(DST_DIR) == False:
		os.mkdir(DST_DIR)
	
	with zipfileSJIS.ZipFile(zipFName) as z:
		z.extractall(path=DST_DIR, pwd=PWD)


# ----------------------------------
# 処理
# ----------------------------------
zipLs = glob.glob('*.zip')
for zipFName in zipLs:
	Unzip(zipFName)
	print('Unziped: ', zipFName)
