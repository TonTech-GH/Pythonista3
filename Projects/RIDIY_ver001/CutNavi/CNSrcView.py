# ==================================
# カットナビゲーター : 必要素材表示
# - 木材カットの良い取回しを提案する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
import os, sys
from os import path
TheDir = path.dirname(path.abspath(__file__))
if (TheDir in sys.path) == False:
	sys.path.append(TheDir)
from CNDef import *

# ----------------------------------
# クラス
# ----------------------------------
class CNSrcView (ui.View):
	# ----------------------------------
	# コンストラクタ
	# param elms 必要素材リスト
	# ----------------------------------
	def __init__(self, elms:list = [], cbEdited = None):
		# 選択肢一覧を表示するTebleViewを生成
		tv = ui.TableView()
		tv.frame = self.bounds
		tv.flex = 'WH'
		tv.row_height = 30
		self.tv = tv
		self.add_subview(self.tv)
		self.SetElms(elms, cbEdited)
		
	# ----------------------------------
	# Elemリストをテーブルビューに適用
	# param elms 必要素材リスト
	# param cbEdited 編集があったときのコールバック
	#  cbEdited(**kwargs)
	#    index : 削除されたインデックス
	# ----------------------------------
	def SetElms(self, elms:list, cbEdited):
		self.elms = elms
		self.cbEdited = cbEdited
		tv = self.tv
		ls = self.ConvElms(elms)
		ds = ui.ListDataSource(ls)
		ds.action = self.item_selected
		ds.edit_action = self.item_edited
		tv.data_source = ds
		tv.delegate = ds
		tv.reload_data()
		
	# ----------------------------------
	# Elemリストを通常のリストに変換
	# ----------------------------------
	def ConvElms(self, elms:list):
		ls = []
		for e in elms:
			s = KindStr[e.kind] + ' : '
			s += str(e.len) + 'mm X ' + str(e.num)
			s += '本'
			ls.append(s)
		return ls
	
	# ----------------------------------
	# アイテム選択時のアクション
	# ----------------------------------
	def item_selected(self, sender):
		item = sender.items[sender.selected_row]
		print(item)
	
	# ----------------------------------
	# アイテム編集時のアクション
	# ----------------------------------
	def item_edited(self, sender):
		# 編集前のリスト
		bf = self.ConvElms(self.elms)
		
		# 編集後のリスト
		af = sender.items
		
		# 長さが変わってなければ終了
		if len(af) == len(bf):
			return 
		
		# 消された要素のインデックスを明らかにする
		idx = -1
		for i in range(0, len(af)):
			if af[i] != bf[i]:
				idx = i
				break
		if idx < 0:
			idx = len(af)
		
		# コールバック関数の呼び出し
		if self.cbEdited != None:
			self.cbEdited(index=idx)
		
# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	v = ui.View()
	v.present('full_screen')
	
	elms = []
	for i in range(1 , 5):
		e = Elem()
		e.kind = Kind.EK_1x4
		e.len  = i * 10
		e.num  = 3
		elms.append(e)
	cnsb = CNSrcView()
	
	def Edited(**kwargs):
		idx = kwargs['index']
		
		for e in elms:	
			print('Bf:', e.kind, e.len, e.num )
		
		e = elms[idx]
		print('del:', e.kind, e.len, e.num )
		
		elms.pop(idx)
		for e in elms:	
			print('Af:', e.kind, e.len, e.num )
		
	cnsb.SetElms(elms, Edited)
	cnsb.frame = (0,0,350,300)
	v.add_subview(cnsb)
	
	
	def Tapped(btn):
		print('\n=== elms ===')
		for e in elms:
			print(e.kind, e.len, e.num)
		
	btn = ui.Button(title='Print')
	btn.frame = (200, 400, 150, 100)
	btn.action = Tapped
	v.add_subview(btn)
