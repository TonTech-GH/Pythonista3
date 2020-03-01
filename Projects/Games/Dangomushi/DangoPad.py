from scene import *
import sound
import random
import math
from collections import namedtuple
import time
import threading
import signal
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

# ループさせるビート
PLAY_BGM = True
BGM = 'sound/loop/Break 02.mp3'

# ループ間隔
LoopTime = 2.385
from mutagen.mp3 import MP3
audio = MP3(BGM)
#LoopTime = audio.info.length #2.455525

LoopTimes = (
	LoopTime * 1/4,
	LoopTime * 2/4,
	LoopTime * 3/4,
	LoopTime,
)

# ダンゴムシ設定
DConf = namedtuple('DConf', 'x,y,se')
DGs = [
	DConf(.15, .75, 'sound/voice/voice_a.mp3'),
	DConf(.50, .75, 'sound/voice/voice_aa.mp3'),
	DConf(.85, .75, 'sound/voice/voice_icecream.mp3'),
	DConf(.15, .50, 'sound/voice/voice_jump.mp3'),
	DConf(.50, .50, 'sound/voice/voice_jump2.mp3'),
	DConf(.85, .50, 'sound/voice/voice_tire.mp3'),
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
		
		# 親と同じサイズに設定
		self.size = parent.size
		self.position = parent.size / 2
		w,h = self.size
		
		# 床を敷く
		elem = SpriteNode()
		elem.texture = Texture('plf:Ground_GrassMid')
		ex, ey = elem.size
		elem.anchor_point = -ex/2, ey/2
		elem.position = -w/2, -200
		elem.size = w, h/2-200
		self.add_child(elem)

'''
シーン
'''
class MyScene (Scene):
	'''
	初期設定
	'''
	def setup(self):
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
			self.finished = False
		
			# 起動予約するメソッド郡
			self.tasks = [self.Beat02, self.Beat03, self.Beat04, self.TimerTask]
			
			# 繰り返し処理用スレッド
			self.thre = []
			self.time = time.time()
		
			# 繰り返し処理の起点
			t=threading.Thread(target=self.TimerTask)
			t.start()
						
	
	'''
	タイマーでの繰り返し処理
	'''
	def TimerTask(self):
		# 関数がコールされた時刻(後で計算に使う)
		st = time.time()
		
		# ループ誤差
		ofst = (st - self.time) - LoopTime
		print(ofst * 1000)
		self.time = st
		
		# 終了判定
		if self.finished:
			return
		
		# 1拍目は即座に実行
		self.Beat01()
		
		# 繰り返し処理の予約
		self.thre = []
		for i, task in enumerate(self.tasks):
			# ここまで来るのにかかった時間
			ofst = time.time() - st
			thre = threading.Timer(LoopTimes[i] - ofst, task)
			thre.start()
			self.thre.append(thre)
		
	'''
	小節内1拍目
	'''
	def Beat01(self): 
		if self.finished:
			return 
		
		#サウンド
		snd = sound.play_effect(BGM)
	
	'''
	小節内2拍目
	'''
	def Beat02(self): 
		if self.finished:
			return
		#sound.play_effect('arcade:Laser_4')
		
	'''
	小節内3拍目
	'''
	def Beat03(self): 
		if self.finished:
			return
		#sound.play_effect('arcade:Laser_4')
	
	'''
	小節内4拍目
	'''
	def Beat04(self): 
		if self.finished:
			return
		#sound.play_effect('arcade:Laser_4')
	
	'''
	バツボタンで閉じられた
	'''
	def stop(self):
		sound.stop_all_effects()
		self.finished = True
	
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
	mys = MyScene()
	run(mys, show_fps=DEBUG)
