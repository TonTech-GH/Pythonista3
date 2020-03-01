# ==================================
# リストからの選択ビュー
# note リストから選択したアイテムをボタンのtitleに反映する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
from UIUtil import *

# ----------------------------------
# クラス
# ----------------------------------
class SelectView (ui.View):
	# ----------------------------------
	# コンストラクタ
	# param ls  選択肢
	# param btn 選択したアイテムを反映するボタン
	# ----------------------------------
	def __init__(self, ls:list, btn:ui.Button):
		# ビュー自体のサイズ指定(popoverで表示するためここでのx,yの値には意味がない)
		self.frame = (0,0,200,140)
		
		# 選択肢一覧を表示するTebleViewを生成
		tv = ui.TableView()
		tv.frame = self.bounds
		tv.flex = 'WH'
		ds = ui.ListDataSource(ls)
		ds.action = self.item_selected
		tv.data_source = ds
		tv.delegate = ds
		self.tableview = tv
		self.add_subview(self.tableview)
		self.name = 'Select'
		
		# ボタンの登録
		self.btn = btn
		
		# 選択完了時に呼び出すコールバックメソッド
		self.cb = None
		
	# ----------------------------------
	# コールバックメソッドの登録
	# ----------------------------------
	def SetCallback(self, cb):
		self.cb = cb
	
	# ----------------------------------
	# 表示
	# param pos 位置を指定する2タプル(x, y)
	# ----------------------------------
	def disp(self, pos=None):
		if pos == None:
			btn = self.btn
			(x, y) = AbsPos(btn)
			x += btn.width / 2
			y += btn.height
			pos = (x, y)
	
		self.present(
			style='popover', 
			popover_location=pos
		)
	
	# ----------------------------------
	# アイテム選択時のアクション
	# ----------------------------------
	def item_selected(self, sender):
		row = sender.selected_row
		item = sender.items[row]
		self.btn.title = item
		if self.cb != None:
			self.cb(index=row)
		self.close()
			
# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	v = ui.View()
	v.present('full_screen')
	
	btn = ui.Button()
	btn.frame = (100,50,150,50)
	btn.background_color = '#d1ff68'
	v.add_subview(btn)

	# --------------------------------
	# ボタンタップ時にテーブルビューをポップオーバー表示
	# --------------------------------
	def Tapped(btn):
		sv = SelectView(['one','two','three'], btn)
		sv.disp()
		
	btn.action = Tapped
