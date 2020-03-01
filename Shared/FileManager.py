import pprint   # 出力文字列の整形用
import pickle	# ファイル保存の標準モジュール
import csv		# CSVファイルの入出力
import shutil	# ディレクトリコピー
import os

# --------------------------------
# ファイルが存在するか
# --------------------------------
def isFileExist(fName):
	return os.path.exists(fName)

# --------------------------------
# 文字列の書き込み
# --------------------------------
def WriteStr(fName : str, strData : str):
	# ファイルオオープン
	f = open(fName, 'w')
	
	# データ書き込み
	f.write(strData)
	
	# ファイルクローズ
	f.close()
		
# --------------------------------
# 任意オブジェクトデータの書き込み
# ※Pythonの標準型以外はエラーになるので注意
# --------------------------------
def WriteObj(fName : str, obj):
	# ファイルオープン
	f = open(fName, 'wb')
	
	# データ書き込み
	pickle.dump(obj, f)
	
	# ファイルクローズ
	f.close()
		
# --------------------------------
# オブジェクトデータの読み込み
# --------------------------------
def ReadObj(fName : str):
	# ファイルオープン
	f = open(fName, 'rb')
	
	# 例外発生時の内容出力関数
	def OutputError(e):
		print("type:{0}".format(type(e)))
		print("args:{0}".format(e.args))
		#print("message:{0}".format(e.message))
		print("{0}".format(e))
		assert False, '例外発生'
		
	# データ読み込み
	try:
		obj = pickle.load(f)
	except pickle.PickleError as e:
		OutputError(e)
	except pickle.UnpicklingError as e:
		OutputError(e)
	except AttributeError as e:
		OutputError(e)
	except EOFError as e:
		OutputError(e)
	except ImportError as e:
		OutputError(e)
	except IndexError as e:
		OutputError(e)
	except :
		assert False, '何らかの例外発生'
	
	# ファイルクローズ
	f.close()
	
	print(type(obj))
	print(obj)
	return obj

# --------------------------------
# 辞書型データをCSVファイルに出力
# fName : ファイル名
# dicLs : 辞書リスト(下記構成を想定)
#   list
#     ├ dict
#     ├ dict
#     ├ dict
# --------------------------------
def SaveCsvDict(fName:str, dicLs:list):
	# キーの抽出
	keys = []
	for k in dicLs[0].keys():
		keys.append(k)
	
	#データ書き込み
	with open(fName, 'w') as f:
		writer = csv.writer(f)
		
		# キーの書き込み
		writer.writerow(keys)
		
		# 実データの書き込み
		for d in dicLs:
			row = []
			for k in keys:
				row.append(d[k])
			writer.writerow(row)

# --------------------------------
# 辞書型データをCSVファイルの読込み
# fName : ファイル名
# --------------------------------
def LoadCsvDict(fName:str):
	dicLs = []
	with open(fName, 'r') as f:
		reader = csv.DictReader(f)
		for d in reader:
			dicLs.append(dict(d))
	return dicLs

# --------------------------------
# ファイルのコピー
# --------------------------------
def CopyFile(srcPath : str, dstPath : str):
	if srcPath == dstPath:
		assert False, 'コピー先に同じパス名は指定出来ない'
		return 
	
	# コピー
	shutil.copy2(srcPath, dstPath)
	
# --------------------------------
# ディレクトリのコピー
# --------------------------------
def CopyDir(srcDir : str, dstDir : str):
	if srcDir == dstDir:
		assert False, 'コピー先に同じディレクトリ名は指定出来ない'
		return 
	
	# ディレクトリをまるっとコピー
	shutil.copytree(srcDir, dstDir)

# --------------------------------
# ディレクトリの削除
# --------------------------------
def RemoveDir(dir : str):
	shutil.rmtree(dir)

# --------------------------------
# ディレクトリの生成
# --------------------------------
def MakeDir(dir : str):
	os.mkdir(dir)

# --------------------------------
# 単体テスト
if __name__ == '__main__':
	fn = 'savedata.csv'
	dicLs = [
		{'kind':1, 'len':123, 'num':1},
		{'kind':2, 'len':123, 'num':1},
		{'kind':3, 'len':123, 'num':1},
		{'kind':4, 'len':123, 'num':1},
		{'kind':5, 'len':123, 'num':1},
	]
	SaveCsvDict(fn, dicLs)
	
	readLs = LoadCsvDict(fn)
	for d in readLs:
		print(d)
