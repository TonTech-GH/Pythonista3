# ==================================
# シンプルなカウンター
#  - カウント値はファイルに保存される
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
import os

# --------------------------------
# 定義
# --------------------------------
#保存ファイル名
fName = 'CountData.txt'

# --------------------------------
# メインクラス
# --------------------------------
class MainView(ui.View):
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		#カウントの読込み
		self.count = 0
		if os.path.exists(fName):
			f = open(fName)
			s = f.read()
			self.count = int(s)
			f.close()
		
	# ----------------------------------
	# ビューのロード完了
	# ----------------------------------
	def did_load(self):
		#ボタンの初期設定
		btn = self['btn_add']
		btn.title = str(self.count)
		btn.action = self.act_btn_add
		
		# ロードとともにカウントを進める
		#self.act_btn_add(btn)

	# ----------------------------------
	# カウント値のセーブ
	# ----------------------------------
	def Save(self):
		f = open(fName, mode='w')
		f.write(str(self.count))
		f.close()
	
	# ----------------------------------
	# カウントアップアクション
	# ----------------------------------
	def act_btn_add(self, btn):
		self.count = self.count + 1
		self.Save()
		btn.title = str(self.count)

# --------------------------------
# メイン
# --------------------------------
if __name__ == '__main__':
	# ビューの生成	
	v = ui.load_view()
	v.present('fullscreen')


