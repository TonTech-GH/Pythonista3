from scene import *
import sound
import random
import math
from collections import namedtuple
from Dango import Dango as DG
A = Action

'''
定義
'''
# デバッグモード
DEBUG = False
def dp(*args):
	if DEBUG == False: return 
	print(args)

# BGM
PLAY_BGM = False
BGM = 'sound/Yakusoku.mp3'

# ダンゴムシ設定
DConf = namedtuple('DConf', 'x,y,se')
DGs = [
	DConf(.15, .75, 'drums:Drums_01'),
	DConf(.50, .75, 'drums:Drums_02'),
	DConf(.85, .75, 'drums:Drums_03'),
	DConf(.15, .50, 'drums:Drums_04'),
	DConf(.50, .50, 'drums:Drums_05'),
	DConf(.85, .50, 'drums:Drums_06'),
	DConf(.15, .25, 'drums:Drums_07'),
	DConf(.50, .25, 'drums:Drums_08'),
	DConf(.85, .25, 'drums:Drums_15'),
]

'''
背景
'''
class MyBG (SpriteNode):
	'''
	初期化
	'''
	def __init__(self, parent, *args, **kwargs):
		super(MyBG, self).__init__(*args, **kwargs)
		self.color = .38, .91, 1.0
		
		self.size = parent.size
		self.position = parent.size / 2
		w,h = self.size
		
		elem = SpriteNode()
		elem.texture = Texture('plf:Ground_GrassMid')
		ex, ey = elem.size
		elem.anchor_point = -ex/2, ey/2
		elem.position = -w/2, -200
		elem.size = w, h/2-200
		self.add_child(elem)

'''
シーン
- タップ判定はすべてここで行われる
'''
class MyScene (Scene):
	'''
	初期設定
	'''
	def setup(self):
		# ビューの設定
		self.background_color = 'green'
		
		# 背景
		bg = MyBG(self)
		self.add_child(bg)
		
		# ダンゴムシの設定
		self.dango = []
		for conf in DGs:
			dango = DG()
			dango.SetSE(conf.se)
			
			w,h = self.size
			dango.position = w * conf.x, h * conf.y
			dango.scale = .40
			self.dango.append(dango)
			self.add_child(dango)
		
		# BGM
		if PLAY_BGM:
			self.bgm = sound.play_effect(BGM, looping=True)
			self.bgm.volume = .2
	
	'''
	バツボタンで閉じられた
	'''
	def stop(self):
		sound.stop_all_effects()
	
	'''
	サイズが変更された
	'''
	def did_change_size(self):
		pass
	
	'''
	更新(毎フレ呼ばれる)
	'''
	def update(self):
		pass
	
	'''
	タッチ開始された
	'''
	def touch_began(self, touch):
		x,y = touch.location
		d = self.dango[0]
		dp('touch' + str(touch.location))
		
		# ダンゴムシタップ判定
		for d in self.dango:
			if d.IsTouch(touch):
				d.ChgeForm(formBall=True)
			else:
				d.ChgeForm(formBall=False)
			
	'''
	ムーブ中
	'''
	def touch_moved(self, touch):
		pass
	
	'''
	タッチがリリースされた
	'''
	def touch_ended(self, touch):
		pass

'''
メイン処理
'''
if __name__ == '__main__':
	run(MyScene(), show_fps=DEBUG)
