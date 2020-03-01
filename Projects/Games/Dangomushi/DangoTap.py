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


'''
シーン
- タップ判定はすべてここで行われる
'''
class MyScene (Scene):
	'''
	初期設定
	'''
	def setup(self):
		# 画面サイズの取得
		dp('size', self.size)
		dp('bounds', self.bounds)
		
		# ビューの設定
		self.background_color = 'green'
		
		# ダンゴムシの設定
		self.dango = []
		dango = DG()
		dango.SetSE(randDrum=True)
		dango.position = self.size / 2
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
		if d.IsTouch(touch):
			d.ChgeForm(formBall=True)
		else:
			# タップした位置にダンゴムシを移動
			d.ChgeForm(formBall=False)
			move_action = Action.move_to(x, y, 0.7, TIMING_SINODIAL)
			d.run_action(move_action)
			sound.play_effect('arcade:Jump_1')
	
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
