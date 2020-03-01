# ==================================
# カットナビゲーター : データ
# - 木材カットの良い取回しを提案する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
# 共通モジュールのインポート
import sys, os
SearchInCur = 'Pythonista3/Documents'
AddDir = '/Shared'
ls = os.getcwd().split(SearchInCur)
sys.path.append(ls[0] + SearchInCur + AddDir)
import FileManager as FM 	# ファイル制御

# 同一ディレクトリのモジュールのインポート
from os import path
TheDir = path.dirname(path.abspath(__file__))
if (TheDir in sys.path) == False:
	sys.path.append(TheDir)
from CNDef import *
from CNBrain import *

# ----------------------------------
# 定義
# ----------------------------------
# 保存ファイル名
SavedCSV = TheDir + '/CNDataSaved.csv'

# ----------------------------------
# カットナビゲーターのデータ
# ----------------------------------
class CNData:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# 必要素材リスト
		self.elms = []
		
		# 最適化結果リスト
		self.resLs = []
		
		# データをファイルからロード
		self.Load()
		
		# 最適化実施
		self.Optimize()
	
	# ----------------------------------
	# 必要素材の追加
	# ----------------------------------
	def AddElem(self, elem:Elem):
		assert isinstance(elem, Elem), 'Elem型以外は追加できない'
		self.elms.append(elem)
		self.Optimize()
		self.Save()
	
	# ----------------------------------
	# 必要素材の削除
	# ----------------------------------
	def DelElem(self, idx:int):
		assert 0 <= idx and idx < len(self.elms), str(idx) + ' is invaliv index'
		self.elms.pop(idx)
		self.Optimize()
		self.Save()
	
	# ----------------------------------
	# アイテムリスト情報の更新
	# ----------------------------------
	def UpdateItems(self, items):
		self.elms = list(items)
		self.Optimize()
		self.Save()
		
	# ----------------------------------
	# データをファイルに保存
	# ----------------------------------
	def Save(self):
		dicLs = []
		for e in self.elms:
			dic = {}
			dic['kind'] = e.kind
			dic['len'] = e.len
			dic['num'] = e.num
			dicLs.append(dic)
		FM.SaveCsvDict(SavedCSV, dicLs)
	
	# ----------------------------------
	# データをファイルからロード
	# ----------------------------------
	def Load(self):
		self.elms = []
		if FM.isFileExist(SavedCSV) == False:
			return 
			
		dicLs = FM.LoadCsvDict(SavedCSV)
		for d in dicLs:
			elm = Elem()
			key = d['kind'].replace('Kind.', '')
			elm.kind = Kind[key]
			elm.len  = int(d['len'])
			elm.num  = int(d['num'])
			self.elms.append(elm)
			
	# ----------------------------------
	# 最適化実施
	# ----------------------------------
	def Optimize(self):
		elms = self.elms
		resLs = Optimize(elms)
		self.resLs = resLs
				
# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	cnd = CNData()
	
	def printCnd():
		print('\n===== CNData =====')
		print(cnd.elms)
		for e in cnd.elms:
			print(e.kind, e.len, e.num)
	
	printCnd()
	elm = Elem()
	elm.len = 1234
	elm.num = 2
	cnd.AddElem(elm)
	
	printCnd()
