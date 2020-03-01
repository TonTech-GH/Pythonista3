# ==================================
# ガルレア周回のデータ蓄積 : 蓄積データ
# - 猫神神社や夢詠みの出現率を測る
# ==================================
# ----------------------------------
# import module
# ----------------------------------
# 共通モジュールのインポート
import sys, os
from datetime import datetime
SearchInCur = 'Pythonista3/Documents'
AddDir = '/Shared'
ls = os.getcwd().split(SearchInCur)
sys.path.append(ls[0] + SearchInCur + AddDir)
import FileManager as FM 	# ファイル制御
from enum import IntEnum, auto

# 専用モジュール
from GalreaDefine import *	# ガルレア定義

# --------------------------------
# ガルレア周回データ(1回分)
# --------------------------------
class Elem:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		self.dID    = None
		self.a1Jin  = 0
		self.a2Jin  = 0
		self.a3Jin  = 0
		self.Gyoku  = 0
		self.Yume   = 0
		self.tenmei = 0
		self.wKey   = 0

# --------------------------------
# ガルレア周回蓄積データ
# --------------------------------
class GalreaData:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# 蓄積ファイルが無かったら作る
		if FM.isFileExist(SaveCSV) == False:
			FM.WriteStr(SaveCSV, '')
		
		# 蓄積データファイルのロード(構造は辞書のリストデータ)
		# list
		#  ├dict
		#  ├dict
		#  ├dict
		self.dictData = FM.LoadCsvDict(SaveCSV)
		
		# 普通のデータ型配列に変換
		# list
		#  ├Elem
		#  ├Elem
		#  ├Elem
		self.elms = self.ConvToElems(self.dictData)
		
	# ----------------------------------
	# 辞書リストをElemリストに変換
	# ----------------------------------
	def ConvToElems(self, dictList):
		elms = []
		for dic in dictList:
			elm = Elem()
			def Val(keyKind):
				return	int(dic[KeyStr[keyKind]])
				
			elm.dID = Val(KeyKind.KK_DID)
			elm.a1Jin = Val(KeyKind.KK_A1_Jin)
			elm.a2Jin = Val(KeyKind.KK_A2_Jin)
			elm.a3Jin = Val(KeyKind.KK_A3_Jin)
			elm.Gyoku = Val(KeyKind.KK_Gyoku)
			elm.Yume = Val(KeyKind.KK_Yume)
			elm.tenmei = Val(KeyKind.KK_TenMei)
			elm.wKey = Val(KeyKind.KK_WKey)
			
			elms.append(elm)
			
		return elms
	
	# ----------------------------------
	# 要素追加
	# ----------------------------------
	def AddElem(self, elem):
		dic = {}
		def SetDic(val, keyKind):
			dic[KeyStr[keyKind]] = val
		
		cur = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		SetDic(cur 				, KeyKind.KK_Date		)
		SetDic(elem.dID   , KeyKind.KK_DID	 	)
		SetDic(elem.a1Jin, KeyKind.KK_A1_Jin)
		SetDic(elem.a2Jin, KeyKind.KK_A2_Jin)
		SetDic(elem.a3Jin, KeyKind.KK_A3_Jin)
		SetDic(elem.Gyoku, KeyKind.KK_Gyoku)
		SetDic(elem.Yume , KeyKind.KK_Yume)
		SetDic(elem.tenmei, KeyKind.KK_TenMei )
		SetDic(elem.wKey  , KeyKind.KK_WKey	  )
		
		self.dictData.append(dic)
		self.Seve()
		
		self.elms = self.ConvToElems(self.dictData)
	
	# ----------------------------------
	# 末尾のデータを削除
	# ----------------------------------
	def DelTail(self):
		tail = self.dictData.pop()
		print('=== Daleted ===')
		print(tail)
		print('===============')
		self.Seve()
		self.elms = self.ConvToElems(self.dictData)
	
	# ----------------------------------
	# データをファイル保存
	# ----------------------------------
	def Seve(self):
		FM.SaveCsvDict(SaveCSV, self.dictData)
	

# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	ADData = GalreaData()
	
	elm = Elem()
	elm : Elem
	elm.dID = 999
	elm.a1Jin = 1
	elm.a2Jin = 2
	elm.a3Jin = 3
	elm.Gyoku = 4
	elm.Yume  = 5
	elm.tenmei = 6
	elm.wKey   = 7
	
	ADData.AddElem(elm)
	
	for d in ADData.dictData:
		print(d)
