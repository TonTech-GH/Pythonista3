# ==================================
# UI生成関連のユーティリティ
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
from collections import namedtuple

# ----------------------------------
# レクト定義
# ----------------------------------
RECT = namedtuple('RECT', 'x,y,w,h')

# ----------------------------------
# UI設定定義
# ----------------------------------
UIConf = namedtuple('UIConf', 'type, title, rect, col, flex')

'''
例:
	UIConf(
		ui.TextField,
		None,
		RECT(0.1, 0.05, 0.55, 0.05),
		'#ffffff',
		'RB',
	)
'''

# ----------------------------------
# UI生成
# ----------------------------------
def CreateUI(parent:ui.View, conf:UIConf):
	# 親となるビュー
	v = parent
	
	# 生成
	assert conf.type != None, 'typeは必須'
	u = conf.type()
	
	# タイトルの設定
	if conf.title != None:
		u.title = conf.title
	
	# 位置、サイズ設定
	# 親ビューに対して相対的な割合で設定
	r = conf.rect
	if v != None and r != None:
		r = (r.x*v.width, r.y*v.height, r.w*v.width, r.h*v.height)
		u.frame = r
	
	# 背景色の設定
	if conf.col != None:
		u.background_color = conf.col
	
	# 拡縮設定
	if conf.flex != None:
		u.flex = conf.flex
	
	# 親子付け
	if v != None:
		v.add_subview(u)
	
	return u

# --------------------------------
# ビューの絶対座標を算出
# retval 位置を示す2タプル(x, y)
# --------------------------------
def AbsPos(view:ui.View):
	x = 0
	y = 0
	curV = view
	while curV != None:
		x += curV.x
		y += curV.y
		curV = curV.superview
	return (x ,y)

# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	print(__file__)
	
	# ビュー生成
	v = ui.View()
	v.present('sheet')
	
	# UI 生成
	ConfLs =[
		# テキストフィールド
		UIConf(
			ui.TextField,
			None,
			RECT(0.1, 0.05, 0.55, 0.05),
			'#ffffff',
			'RB',
		),
		
		# テーブルビュー(必要数表示用)
		UIConf(
			ui.TableView,
			None,
			RECT(0.1, 0.11, 0.8, 0.29),
			'#ffffff',
			'WHB',
		),
		
		# テーブルビュー(結果表示用)
		UIConf(
			ui.TableView,
			None,
			RECT(0.1, 0.55, 0.8, 0.4),
			'#ffffff',
			'WHT',
		),
		
		# 追加ボタン
		UIConf(
			ui.Button, 
			'ADD!',
			RECT(0.7, 0.05, 0.2, 0.05), 
			'#ffaf45',
			'RB',
		),
		
		# 計算ボタン
		UIConf(
			ui.Button, 
			'↓NAVI↓',
			RECT(0.35, 0.45, 0.3, 0.05), 
			'#ffaf45',
			'LRTB',
		),
	]
	for conf in ConfLs:
		u = CreateUI(v, conf)
	
	
