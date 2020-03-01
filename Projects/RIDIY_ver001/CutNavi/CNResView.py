# ==================================
# カットナビゲーター : 結果表示
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
# 定義
# ----------------------------------
# 画像の置き場所
IMG_DIR = TheDir + '/img'

# 画像名
IMG_NAMES = (
	'Wood01.JPG',
	'Wood02.JPG',
	'Wood03.JPG',	
)

# 色
COL_MTL = (.92, .81, .67, .0)	# 必要素材の色
COL_MGN = (.04, .62, 1.0, .3)	# マージンの色

# ----------------------------------
# クラス
# ----------------------------------
class CNResView(ui.View):
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# ビュー設定
		self.background_color = 1.0, 1.0, 1.0, .4
		
	# ----------------------------------
	# 結果データをセット
	# ----------------------------------
	def SetResData(self, reses):
		# 表示設定
		offX = 20
		offY = 20
		gapY = 10
		wid = self.width - offX * 2
		hei = 30
		rows = len(reses)
		
		# スクロールビュー生成
		sv = ui.ScrollView()
		sv.frame = self.bounds
		sv.content_size = (sv.width, offY * 2 + hei * rows + gapY * (rows - 1))
		sv.background_color = 1.0, .87, .74, .4
		self.add_subview(sv)
		self.sv = sv
		
		# 要素表示生成メソッド
		def CreateMtlV(row, wLen, l, curX):
			btn = ui.Button()
			eWid = wid * l / wLen
			btn.frame = (offX + curX, offY + (hei+gapY) * row, eWid, hei)
			btn.border_width = 1
			btn.border_color = '#000000'
			btn.title = str(int(l))
			
			curX += eWid
			return curX, btn
		
		# 表示追加
		for i in range(0, rows):
			mtl = reses[i]
			
			# 全体長さの表示
			tmp, btn = CreateMtlV(i, mtl.len, mtl.len, 0)
			btn.title = ''
			imgIdx = i % len(IMG_NAMES)
			imgPath = IMG_DIR + '/' + IMG_NAMES[imgIdx]
			img = ui.Image.named(imgPath)
			btn.background_image = img
			self.sv.add_subview(btn)
			
			# 必要素材の表示
			curX = 0
			for l in mtl.cls:
				curX, btn = CreateMtlV(i, mtl.len, CUT_MARGIN, curX)
				btn.background_color = COL_MGN
				btn.title = ''
				self.sv.add_subview(btn)
				
				curX, btn = CreateMtlV(i, mtl.len, l, curX)
				btn.background_color = COL_MTL
				btn.tint_color = '#29519c'
				self.sv.add_subview(btn)
			
			# 残り長さの表示
			l = mtl.len - mtl.TtlLen()
			curX, btn = CreateMtlV(i, mtl.len, l, curX)
			btn.background_color = COL_MGN
			btn.tint_color = '#434547'
			self.sv.add_subview(btn)
			

# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	v = ui.View()
	v.present('fullscreen')
	
	reses = []
	for i in range(0, 10):
		mtl = Material()
		mtl.kind = Kind.EK_1x4
		mtl.cls = [l for l in range(200, 600, 100)]
		reses.append(mtl)
	
	frame = (20, 20, v.width-40, v.height/2)
	cnrv = CNResView()
	cnrv.frame = frame
	cnrv.SetResData(reses)
	
	v.add_subview(cnrv)


