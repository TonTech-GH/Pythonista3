# ==================================
# アナダン周回のデータ蓄積 : 蓄積データ
# - レアエリアや夢詠みの出現率を測る
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
from AnadanDefine import *	# アナダン定義

# --------------------------------
# アナダン周回データ(1回分)
# --------------------------------
class Elem:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		self.dID = None
		self.a2Rare = 0
		self.a2Yume = 0
		self.a3Rare = 0
		self.a3Yume = 0
		self.pbYume = 0
		self.tenmei = 0
		self.wKey   = 0

# --------------------------------
# アナダン周回蓄積データ
# --------------------------------
class AnadanData:
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
				
			elm.dID    = Val(KeyKind.KK_DID)
			elm.a2Rare = Val(KeyKind.KK_A2_Rare)
			elm.a2Yume = Val(KeyKind.KK_A2_Yume)
			elm.a3Rare = Val(KeyKind.KK_A3_Rare)
			elm.a3Yume = Val(KeyKind.KK_A3_Yume)
			elm.pbYume = Val(KeyKind.KK_PB_Yume)
			elm.tenmei = Val(KeyKind.KK_TenMei)
			elm.wKey   = Val(KeyKind.KK_WKey)
			
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
		SetDic(elem.a2Rare, KeyKind.KK_A2_Rare)
		SetDic(elem.a2Yume, KeyKind.KK_A2_Yume)
		SetDic(elem.a3Rare, KeyKind.KK_A3_Rare)
		SetDic(elem.a3Yume, KeyKind.KK_A3_Yume)
		SetDic(elem.pbYume, KeyKind.KK_PB_Yume)
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
	#本データに悪影響しないようにリネーム
	SaveCSV = 'デバッグ用ダミー周回データ.csv'
	
	#生成
	ADData = AnadanData()
	
	#ダミーデータ追加
	elm = Elem()
	elm : Elem
	elm.dID = 999
	elm.a2Rare = 1
	elm.a2Yume = 2
	elm.a3Rare = 3
	elm.a3Yume = 4
	elm.pbYume = 5
	elm.tenmei = 6
	elm.wKey   = 7
	#ADData.AddElem(elm)
	
	#末尾のデータ削除
	#ADData.DelTail()
	
	#for d in ADData.dictData:
	#	print(d)
	
