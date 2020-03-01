# --------------------------------
# プロジェクトのバックアップ
# 過去のバックアップ先ディレクトリをき
# すべてのファイルとフォルダをバックアップする
# --------------------------------
import Shared.FileManager as fm
from datetime import datetime # 現在時刻取得
from pathlib import Path # ファイルリスト取得
import os
import console	# ダイアログ表示

# --------------------------------
# 定義
# --------------------------------
# バックアップ先ディレクトリ名のベース
DST_NAME_BASE = 'BackUp_'

# バックアップから除外する文字列
SKIP_NAME = '.Trash'

# --------------------------------
# コピー先ディレクトリ名の構築
# --------------------------------
def DstDirName():
	name = DST_NAME_BASE
	
	# 現在時刻をくっつける
	time = datetime.now()
	timeStr = time.strftime('%Y%m%d_%H%M')
	return name + timeStr

# --------------------------------
# コピー対象のファイルリスト取得
# --------------------------------
def FilesForCopy():
	# 対象の拡張子リスト
	extLs = ['*.py', '*.pyui', '*.PNG']
	
	# ファイルリスト構築
	ls = []
	p = Path('./')
	for ext in extLs:
		pathLs = p.glob(ext)
		for elem in pathLs:
			ls.append(elem.name)
	return ls

# --------------------------------
# バックアップ実施
# --------------------------------
if __name__ == '__main__':
	# 保存先のディレクトリ生成
	dstName = DstDirName()
	#print(dstName)
	Path(dstName).mkdir()
	
	# ファイルとフォルダをリストアップ
	cd = os.getcwd()
	lsdir = os.listdir(cd)
	#print(lsdir)
	
	skipped = []
	buFile = []
	buFolder = []
	# バックアップ実施
	for d in lsdir:
		# バックアップ先フォルダは除外
		if DST_NAME_BASE in d:
			skipped.append(d)
			continue		
		# 特定文字列を含むものは除外
		if SKIP_NAME in d:
			skipped.append(d)
			continue
		
		# 対象のフルパス
		fpass = cd + '/' + d
		src = d
		dst = dstName + '/' +d
		
		# コピー実施
		if os.path.isdir(fpass):
			#フォルダ
			buFolder.append(d)
			fm.CopyDir(src, dst)
		else:
			# ファイル
			buFile.append(d)
			fm.CopyFile(src, dst)
		
	# 結果出力
	msg = ''
	msg += '\n===== Back UP Done =====\n'
	for f in buFolder:
		msg += f + '\n'
	for f in buFile:
		msg += f + '\n'
	
	msg += '\n===== Skipped =====\n'
	for f in skipped:
		msg += f + '\n'
	
	# ダイアログ表示
	console.alert(msg, '', 'OK', hide_cancel_button=True)
