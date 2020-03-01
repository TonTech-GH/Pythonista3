# ==================================
# カットナビゲーター : 表示メイン
# - 木材カットの良い取回しを提案する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
from collections import namedtuple
from enum import IntEnum, auto
import os, sys
from os import path
TheDir = path.dirname(path.abspath(__file__))
if (TheDir in sys.path) == False:
	sys.path.append(TheDir)
from CNDef import *
from CNData import CNData as CND
from CNSrcView import  CNSrcView as CNSV
from CNResView import  CNResView as CNRV
	
# 共通モジュールのインポート
SearchInCur = 'Pythonista3/Documents'
AddDir = '/Shared'
ls = os.getcwd().split(SearchInCur)
sys.path.append(ls[0] + SearchInCur + AddDir)
import FileManager as FM 	# ファイル制御
import UIUtil as UT	# UIユーティリティ
from SelectView import SelectView as SV

# ----------------------------------
# UI設定
# ----------------------------------
# ビュー設定
ViewConf = UT.UIConf(
	ui.View,
	'CUT NAVI',
	None,
	'#ffffff',
	None,
)

# 子UIの識別子
class UIs(IntEnum):
	MAIN_BG= auto()
	BT_Kind= auto()
	TF_Len = auto()
	BT_Num = auto()
	TV_Src = auto()
	TV_Res = auto()
	BT_Add = auto()

# 子UI設定
ConfDict ={
	# 背景
	UIs.MAIN_BG:
	UT.UIConf(
		ui.Button, 
		'',
		UT.RECT(0, 0, 1.0, 1.0), 
		'#ffffff',
		'WH',
	),
	
	# 追加ボタン
	UIs.BT_Kind:
	UT.UIConf(
		ui.Button, 
		'1x4',
		UT.RECT(0.1, 0.05, 0.09, 0.05), 
		'#ffffff',
		'RB',
	),
	
	# テキストフィールド(長さ)
	UIs.TF_Len:
	UT.UIConf(
		ui.TextField,
		None,
		UT.RECT(0.2, 0.05, 0.15, 0.05),
		'#ffffff',
		'RB',
	),
	
	# テキストフィールド(数)
	UIs.BT_Num:
	UT.UIConf(
		ui.Button,
		'1',
		UT.RECT(0.4, 0.05, 0.10, 0.05),
		'#ffffff',
		'RB',
	),
	
	# テーブルビュー(必要数表示用)
	UIs.TV_Src:
	UT.UIConf(
		CNSV,
		None,
		UT.RECT(0.1, 0.11, 0.8, 0.29),
		(1.0, 1.0, 1.0),
		'WHB',
	),
	
	# テーブルビュー(結果表示用)
	UIs.TV_Res:
	UT.UIConf(
		CNRV,
		None,
		UT.RECT(0.1, 0.45, 0.8, 0.5),
		None,
		'WHT',
	),
	
	# 追加ボタン
	UIs.BT_Add:
	UT.UIConf(
		ui.Button, 
		'ADD!',
		UT.RECT(0.7, 0.05, 0.2, 0.05), 
		'#ffaf45',
		'LB',
	),
}

# ----------------------------------
# カットナビゲーターの表示メイン
# ----------------------------------
class CNView:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self, cnd:CND):
		self.cnd = cnd
		self.Setting()
	
	# ----------------------------------
	# UI生成
	# ----------------------------------
	def Setting(self):
		# ビューの生成
		v = UT.CreateUI(None, ViewConf)
		v.present('full_screen')
		self.v = v	
		
		# UIの生成
		self.u = {}
		for k,conf in ConfDict.items():
			u = UT.CreateUI(v, conf)
			u.alpha = .925
			self.u[k] = u
		
		# 個別設定 +++++++++++++++++++
		# 背景
		bg = self.u[UIs.MAIN_BG]
		img = ui.Image.named(TheDir + '/img/CNBG.JPG')
		bg.background_image = img
		bg.enabled = False
		
		self.SetTableView()
		self.u[UIs.BT_Kind].action = self.KindTapped
		self.u[UIs.BT_Num].action = self.NumTapped
		self.u[UIs.BT_Add].action = self.AddTapped
		self.u[UIs.TF_Len].keyboard_type = ui.KEYBOARD_NUMBERS
	
	# ----------------------------------
	# テーブルビューの設定
	# ----------------------------------
	def SetTableView(self):
		# 必要素材のテーブルビュー
		elms = self.cnd.elms
		self.SetTableViewSrc(elms)
		
		# 結果のテーブルビュー
		resLs = self.cnd.resLs
		self.SetTableViewRes(resLs)
		
	# ----------------------------------
	# 必要素材のテーブルビュー設定
	# ----------------------------------
	def SetTableViewSrc(self, elms):
		tv = self.u[UIs.TV_Src]
		
		# リストが編集されたときのコールバック
		def cbEdited(**kwargs):
			idx = kwargs['index']
			self.cnd.DelElem(idx)
			self.SetTableView()
			
		tv.SetElms(elms, cbEdited)
	
	# ----------------------------------
	# 最適な取回しのテーブルビュー設定
	# ----------------------------------
	def SetTableViewRes(self, resLs:list):
		resV = self.u[UIs.TV_Res]
		resV.SetResData(resLs)
	
	# ----------------------------------
	# 素材種別ボタンタップ時のアクション
	# ----------------------------------
	def KindTapped(self, btn:ui.Button):
		ls = []
		for val in KindStr.values():
			ls.append(val)
		sv = SV(ls, btn)
		sv.disp()
	
	# ----------------------------------
	# 数量ボタンタップ時のアクション
	# ----------------------------------
	def NumTapped(self, btn:ui.Button):
		ls = []
		for i in range(1, 11):
			ls.append(str(i))
		sv = SV(ls, btn)
		sv.disp()
	
	# ----------------------------------
	# 追加ボタンタップ時のアクション
	# ----------------------------------
	def AddTapped(self, btn:ui.Button):
		bk = self.u[UIs.BT_Kind]
		tf = self.u[UIs.TF_Len]
		bn = self.u[UIs.BT_Num]
		
		# 素材種別を引いてくる
		kind = None
		for key,val in KindStr.items():
			if val == bk.title:
				kind = key
		
		if tf.text.isdigit():
			elm = Elem()
			elm.kind= kind
			elm.len = int(tf.text)
			elm.num = int(bn.title)
			
			self.cnd.AddElem(elm)
			self.SetTableView()
		
		tf.text = ''
	
# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	cnd = CND()
	cnv = CNView(cnd)
	
