# ==================================
# ガルレア周回のデータ蓄積
# - レアエリアや夢詠みの出現率を測る
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import ui
from enum import IntEnum, auto

# 共通モジュールのインポート
import sys, os
SearchInCur = 'Pythonista3/Documents'
AddDir = '/Shared'
ls = os.getcwd().split(SearchInCur)
sys.path.append(ls[0] + SearchInCur + AddDir)
import SelectView as SV   # 選択ビュー

# 専用モジュール
from GalreaDefine import Master	# ガルレア定義
from GalreaData   import GalreaData, Elem

# --------------------------------
# 定義
# --------------------------------
# 初期ダンジョンインデックス
DefaultIdx = 1

# UI種別
class UIKind(IntEnum):
	SegCon_A1 		 = auto()	# エリア1のセグメントコントロール
	SegCon_A2 		 = auto()	# エリア2のセグメントコントロール
	SegCon_A3 		 = auto()	# エリア3のセグメントコントロール
	SegCon_Gyoku 	 = auto() # 攻撃の硬玉のセグメントコントロール
	SegCon_Yume 	 = auto() # 夢詠みの書のセグメントコントロール
	SegCon_up      = auto() # 天冥値アップのセグメントコントロール
	SegCon_wKey    = auto() # 白鍵のセグメントコントロール
	BtnLoc         = auto() # 場所選択ボタン
	BtnAdd         = auto() # 追加ボタン
	BtnCancel      = auto() # 取消ボタン
	TvSum          = auto() # まとめテキストビュー
	BtnBG          = auto() # 背景表示用ボタン

# UI定義
UIDict = {
	UIKind.SegCon_A1 			: 'segCon_a1',
	UIKind.SegCon_A2 			: 'segCon_a2',
	UIKind.SegCon_A3 			: 'segCon_a3',
	UIKind.SegCon_Gyoku 	: 'segCon_gyoku',
	UIKind.SegCon_Yume 		: 'segCon_yume',
	UIKind.SegCon_up 			: 'segCon_up',
	UIKind.SegCon_wKey		: 'segCon_wKey',
	UIKind.BtnLoc 				: 'btnLoc',
	UIKind.BtnAdd 				: 'btnAdd',
	UIKind.BtnCancel 			: 'btnCancel',
	UIKind.TvSum 					: 'tvSum',
	UIKind.BtnBG 					: 'btn_BG',
}

# --------------------------------
# ガルレア周回まとめクララス
# --------------------------------
class GalreaSum:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# 変数の初期化
		self.selView = None
		
		# ビューの生成	
		v = ui.load_view()
		v.present('fullscreen')
		self.view = v
		
		# 取消しボタンはデータ追加するまでは無効
		btn = self.GetUI(UIKind.BtnCancel)
		btn.enabled = False
		
		# 背景の設定
		btn = self.GetUI(UIKind.BtnBG)
		img = ui.Image.named('img/bg00.PNG')
		btn.background_image = img
		btn.enabled = False
		
		# データの生成
		self.data = GalreaData()
		
		# 現在のダンジョンマスター情報
		self.master = Master[DefaultIdx]
		
		# ダンジョン種別をセット
		str = self.master.name
		self.GetUI(UIKind.BtnLoc).title = str
		
		# サマリ表示の更新
		self.UpdateUI(self.master)
	
	# --------------------------------
	# メンバ関数
	# --------------------------------
	# サブビューの取得
	def GetUI(self, kind):
		str = UIDict[kind]
		return self.view[str]
	
	# マスター情報を表示に反映
	def UpdateUI(self, master):
		# セグメントコントロールの更新
		segConfs = [
			UIKind.SegCon_A1,
			UIKind.SegCon_A2,
			UIKind.SegCon_A3,
		]
		for kind in segConfs:
			seg = self.GetUI(kind)
			idx = seg.selected_index
			seg.segments = ('通常', master.rareName)
			seg.selected_index = idx
		
		# 追加ボタンの更新
		btn = self.GetUI(UIKind.BtnAdd)
		btn.enabled = master.addable
		
		# ダンジョン選択ボタンの更新
		btn = self.GetUI(UIKind.BtnLoc)
		img = ui.Image.named('img/' + master.banner)
		btn.background_image = img
		btn.title = ''
		
		# サマリー表示の更新
		self.UpdateSum(master)
	
	# サマリ表示の更新
	def UpdateSum(self, master):
		# 該当するダンジョンIDの履歴をかき集める
		dID = master.dID
		sum = Elem()
		cnt = 0
		for elm in self.data.elms:
			if elm.dID != dID and dID != 0:
				continue
			cnt = cnt + 1
			sum.a1Jin += elm.a1Jin
			sum.a2Jin += elm.a2Jin
			sum.a3Jin += elm.a3Jin
			sum.Gyoku += elm.Gyoku
			sum.Yume  += elm.Yume
			sum.tenmei += elm.tenmei
			sum.wKey 	 += elm.wKey
		
		# ここから表示更新
		tv = self.GetUI(UIKind.TvSum)
		
		# 周回数0なら何も表示しない
		if cnt <= 0:
			tv.text = '周回数 : 0'
			return 
		
		txt = ''
		txt += '周回数 : ' + str(cnt) + '\n'
		def Txt(lbl, val):
			tmp = ''
			tmp += lbl + ' : ' + str(val)
			rate = val / cnt * 100
			rate = round(rate, 2)
			tmp += ' (' + str(rate) + '%)'
			tmp += '\n'
			return tmp
		
		txt+=Txt('エリア1' + master.rareName, sum.a1Jin)
		txt+=Txt('エリア2' + master.rareName, sum.a2Jin)
		txt+=Txt('エリア3' + master.rareName, sum.a3Jin)
		txt+=Txt('攻撃の硬玉    ', sum.Gyoku)
		txt+=Txt('夢詠みの書    ',sum.Yume)
		txt+=Txt('天冥値アップ   ',sum.tenmei)
		txt+=Txt('ホワイトキー   ',sum.wKey)
		tv.text = txt
		
	# --------------------------------
	# アクション
	# --------------------------------
	# 場所ボタンタップ時の処理
	def BtnLoc_Tapped(self, btn):
		# 選択ビュー
		selLs = []
		for elem in Master:
			selLs.append(elem.name)
		
		selView = SV.SelectView(selLs, btn)
		selView.SetCallback(self.Loc_Selected)
		selView.disp()
	
	# 場所選択後の処理
	def Loc_Selected(self, **kwargs):
		# 選択されたインデックスに対応するマスターに切替え
		master = self.master
		if 'index' in kwargs:
			idx = kwargs['index']
			master = Master[idx]
		self.master = master
		
		#表示の更新
		self.UpdateUI(master)
	
	# 追加ボタンタップ時の処理
	def BtnAdd_Tapped(self, btn):
		elm = Elem()
		
		# ボタンは1起動で1回しか押させない
		btn.enabled = False
		btn.background_color = (0.2)
		
		# ダンジョンID
		elm.dID = self.master.dID
		
		# エリア1
		idx = self.GetUI(UIKind.SegCon_A1).selected_index
		elm.a1Jin = 1 if idx >= 1 else 0
		
		# エリア2
		idx = self.GetUI(UIKind.SegCon_A2).selected_index
		elm.a2Jin = 1 if idx >= 1 else 0
		
		# エリア3
		idx = self.GetUI(UIKind.SegCon_A3).selected_index
		elm.a3Jin = 1 if idx >= 1 else 0
		
		# 硬玉
		idx = self.GetUI(UIKind.SegCon_Gyoku).selected_index
		elm.Gyoku = idx
		
		# 夢詠みの書
		idx = self.GetUI(UIKind.SegCon_Yume).selected_index
		elm.Yume = idx
		
		# 天冥値
		idx = self.GetUI(UIKind.SegCon_up).selected_index
		elm.tenmei = 1 if idx >= 1 else 0
		
		# 白鍵
		idx = self.GetUI(UIKind.SegCon_wKey).selected_index
		elm.wKey   = 1 if idx >= 1 else 0
		
		#print(elm.dID, elm.a1Jin, elm.a2Jin, elm.a3Jin, elm.Gyoku, elm.Yume, elm.tenmei, elm.wKey)
		self.data.AddElem(elm)
		
		self.UpdateSum(self.master)
		
		# 取消しボタンを有効化
		self.GetUI(UIKind.BtnCancel).enabled = True
		
	# 取消しボタンタップ時の処理
	def BtnCancel_Tapped(self, btn):
		self.data.DelTail()
		self.UpdateSum(self.master)
		btn.enabled = False

# --------------------------------
# メイン
# --------------------------------
if __name__ == '__main__':
	mainView = GalreaSum()

