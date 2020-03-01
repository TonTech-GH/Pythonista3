from scene import *
import sound
import random
import math
import random
A = Action

'''
定義
'''
# デバッグモード
DEBUG = False
def dp(*args):
	if DEBUG == False: return 
	print(args)

# 画像
IMG_DANGO_NML  = 'img/dango01.PNG'
IMG_DANGO_BALL = 'img/dango02.PNG'

# 効果音
def RandDrum():
	name = 'drums:Drums_'
	no = random.randrange(0,16) + 1
	name += '{:02}'.format(no)
	return name

'''
テクスチャ
'''
TexNormal = Texture(IMG_DANGO_NML)
TexBall   = Texture(IMG_DANGO_BALL)

'''
ダンゴムシノード
'''
class Dango (SpriteNode):
	'''
	初期化
	touchSE=None : タッチ時のSE指定
	randDrum=False : タッチ時のSEをランダムドラムにする
	'''
	def __init__(self, *args, **kwargs):
		super(Dango, self).__init__(*args, **kwargs)
		
		self.scale = .5
		self.texture = TexNormal
		self.bBall = False
		self.se = None
		self.randDrum = False
		self.SetSE()
	
	'''
	タッチ時の効果音を設定
	se : SE指定
	randDrum=False : タッチ時のSEをランダムドラムにする
	'''	
	def SetSE(self, se=None, **kwargs):
		self.se = se
		key = 'randDrum'
		if key in kwargs:
			self.randDrum = kwargs[key]
		
	'''
	通常とダンゴの表示切替え
	kwdargs formBall=False ※指定しなければトグル切替え
	'''
	def ChgeForm(self, **kwargs):
		key = 'formBall'
		if key in kwargs:
			self.bBall = kwargs[key]
		elif self.bBall:
			self.bBall = False
		else:
			self.bBall = True
			
		tex = TexNormal
		if self.bBall: tex = TexBall
		self.texture = tex
	
	'''
	タッチされたか？
	'''
	def IsTouch(self, touch):
		x,y,w,h = self.frame
		tx,ty = touch.location
		dp('Dango frame', self.frame)
		
		# タッチ判定
		bTouch = touch.location in self.frame
		if bTouch == False: return False
		
		# 効果音
		se = self.se
		if self.randDrum: se = RandDrum()
		if se != None:
			sound.play_effect(se, volume=5.0)
		return True

'''
単体テスト
'''
if __name__ == '__main__':
	'''
	テストシーン
	'''
	class TestScene (Scene):
		'''
		初期設定
		'''
		def setup(self):
			# ダンゴムシの設定
			dango = Dango()
			#dango.SetSE(randDrum=True)
			#dango.SetSE()
			dango.SetSE('arcade:Coin_2')
			dango.position = self.size / 2
			self.dango = dango
			self.add_child(dango)
		
		'''
		バツボタンで閉じられた
		'''
		def stop(self):
			sound.stop_all_effects()
		
		'''
		タッチ開始された
		'''
		def touch_began(self, touch):
			# ダンゴムシタップ判定
			d = self.dango
			if d.IsTouch(touch):
				d.ChgeForm(formBall=True)
			else:
				# タップした位置にダンゴムシを移動
				d.ChgeForm(formBall=False)
		
	run(TestScene(), show_fps=DEBUG)
	
