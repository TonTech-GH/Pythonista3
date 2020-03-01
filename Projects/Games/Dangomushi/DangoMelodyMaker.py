import ui
import sound
from collections import namedtuple
from KeySound import MKey

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
ビュー
'''
class MyView (ui.View):
	'''
	初期設定
	'''
	def __init__(self):
		self.present('fullscreen')
		self.background_color = .92, 1.0, .95
		self.keys = []
		self.btn = []

		# 鍵盤の基準位置、幅高さ
		kw = self.width / (len(MKey) + 2)
		kh = self.height * .3
		kx = kw
		ky = self.height * .2

		# 鍵盤の生成
		for idx, (key, conf) in enumerate(MKey.items()):
			btn = ui.Button()

			# 見た目の設定
			btn.background_color = 1.0, 1.08, 1.08
			btn.border_color = .0, .0, .0
			btn.border_width = 1

			# 位置サイズ
			btn.frame = (kx + kw*idx, ky, kw, kh)

			# キー鳴らす設定
			btn.title = key
			btn.action = self.KeyTapped
			self.btn.append(btn)
			self.add_subview(btn)

		# テキストフィールド
		tv = ui.TextView()
		tv.frame = (kx, self.height*.6, kx*len(MKey), self.height*.35)
		tv.editable = False
		self.tv = tv
		self.add_subview(tv)

		# 戻るボタン
		backB = ui.Button()
		backB.background_color = 1.0, .87, .69
		backB.frame = (kx, self.height*.05, self.width*.2, self.height*.05)
		backB.title = '1つ消す'
		backB.action = self.BackTapped
		self.backB = backB
		self.add_subview(backB)

		# 改行ボタン
		retB = ui.Button()
		retB.background_color = 1.0, .87, .69
		retB.frame = (self.width*.8-kw, self.height*.05, self.width*.2, self.height*.05)
		retB.title = '改行'
		retB.action = self.RetTapped
		self.retB = retB
		self.add_subview(retB)

	'''
	ビューがで閉じられた
	'''
	def stop(self):
		sound.stop_all_effects()

	'''
	鍵盤が押された
	'''
	def KeyTapped(self, btn):
		# 押されたキー
		key = btn.title

		# 押した鍵盤の音を鳴らす
		conf = MKey[key]
		sound.play_effect(conf.file)

		# 押したキーの記録
		self.keys.append(key)
		self.UpdateTV()

	'''
	1つ消すボタン
	'''
	def BackTapped(self, btn):
		sound.play_effect('ui:switch30')
		if len(self.keys) <= 0: return
		self.keys.pop(-1)
		self.UpdateTV()

	'''
	改行ボタン
	'''
	def RetTapped(self, btn):
		sound.play_effect('ui:switch33')
		self.keys.append('\n')
		self.UpdateTV()

	'''
	テキストビューの更新
	'''
	def UpdateTV(self):
		text = ''
		keys = self.keys
		for key in keys:
			if key == '\n':
				text += key
				continue
			text += '\'' + key + '\', '

		self.tv.text = text

'''
メイン処理
'''
if __name__ == '__main__':
	v = MyView()
