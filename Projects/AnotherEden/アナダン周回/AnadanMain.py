# ==================================
# アナダン周回のデータ蓄積
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
from AnadanDefine import *	# アナダン定義
from AnadanData   import AnadanData, Elem

# --------------------------------
# 定義
# --------------------------------
# 初期ダンジョンインデックス
DefaultIdx = 4

# UI種別
class UIKind(IntEnum):
	SegCon_A2 		 = auto()	# エリア2のセグメントコントロール
	SegCon_A3 		 = auto()	# エリア3のセグメントコントロール
	SegCon_preBoss = auto() # ボス前宝箱のセグメントコントロール
	SegCon_up      = auto() # 天冥値アップのセグメントコントロール
	SegCon_wKey    = auto() # 白鍵のセグメントコントロール
	BtnLoc         = auto() # 場所選択ボタン
	BtnAdd         = auto() # 追加ボタン
	BtnCancel      = auto() # 取消ボタン
	TvSum          = auto() # まとめテキストビュー

# UI定義
UIDict = {
	UIKind.SegCon_A2 			: 'segCon_a2',
	UIKind.SegCon_A3 			: 'segCon_a3',
	UIKind.SegCon_preBoss : 'segCon_preBoss',
	UIKind.SegCon_up 			: 'segCon_up',
	UIKind.SegCon_wKey		: 'segCon_wKey',
	UIKind.BtnLoc 				: 'btnLoc',
	UIKind.BtnAdd 				: 'btnAdd',
	UIKind.BtnCancel 			: 'btnCancel',
	UIKind.TvSum 					: 'tvSum',
}

# --------------------------------
# アナダン周回まとめクララス
# --------------------------------
class AnadanSum:
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
		
		# データの生成
		self.data = AnadanData()
		
		# 現在のダンジョンマスター情報
		self.master = Master[DefaultIdx]
		
		# ダンジョン種別をセット
		str = self.master.name
		self.GetUI(UIKind.BtnLoc).title = str
		
		# 表示の更新
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
		#セグメントコントロールの更新
		segA2 = self.GetUI(UIKind.SegCon_A2)
		idx = segA2.selected_index
		segA2.segments = (master.a2n, master.a2r, '夢詠み')
		segA2.selected_index = idx
		
		segA3 = self.GetUI(UIKind.SegCon_A3)
		idx = segA3.selected_index
		segA3.segments = (master.a3n, master.a3r, '夢詠み')
		segA3.selected_index = idx
		
		#追加ボタンの更新
		btn = self.GetUI(UIKind.BtnAdd)
		btn.enabled = master.addable
		
		#ダンジョン選択ボタンの更新
		btn = self.GetUI(UIKind.BtnLoc)
		img = ui.Image.named('img/' + master.banner)
		btn.background_image = img
		btn.title = ''
		
		#サマリ表示の更新
		self.UpdateSum(master)
	
	# サマリ表示の更新
	def UpdateSum(self, master):
		#該当するダンジョンIDの履歴をかき集める
		dID = master.dID
		sum = Elem()
		cnt = 0
		tenmeiCnt=0
		for elm in self.data.elms:
			if elm.dID != dID and dID != 0:
				continue
			cnt = cnt + 1
			sum.a2Rare += elm.a2Rare
			sum.a2Yume += elm.a2Yume
			sum.a3Rare += elm.a3Rare
			sum.a3Yume += elm.a3Yume
			sum.pbYume += elm.pbYume
			
			# 天冥は編成無し（2）を考慮
			if elm.tenmei == 1:
				sum.tenmei += elm.tenmei
			if elm.tenmei != 2:
				tenmeiCnt += 1
				
			sum.wKey 	 += elm.wKey
		
		#ここから表示更新
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
		
		txt+=Txt('エリア2レア    ',sum.a2Rare)
		txt+=Txt('エリア2夢詠み',sum.a2Yume)
		txt+=Txt('エリア3レア    ',sum.a3Rare)
		txt+=Txt('エリア3夢詠み',sum.a3Yume)
		txt+=Txt('ボス前夢詠み   ',sum.pbYume)
		
		# 天冥アップは編成無しを考慮
		txt+='天冥値アップ    : '
		txt+= str(sum.tenmei)
		txt+= '/' + str(tenmeiCnt)
		rate = sum.tenmei / tenmeiCnt * 100
		rate = round(rate, 2)
		txt += ' (' + str(rate) + '%)\n'
		
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
		
		# エリア2
		idx = self.GetUI(UIKind.SegCon_A2).selected_index
		elm.a2Rare = 1 if idx >= 1 else 0
		elm.a2Yume = 1 if idx >= 2 else 0 
		
		# エリア3
		idx = self.GetUI(UIKind.SegCon_A3).selected_index		
		elm.a3Rare = 1 if idx >= 1 else 0
		elm.a3Yume = 1 if idx >= 2 else 0

		# ボス前夢詠み
		idx = self.GetUI(UIKind.SegCon_preBoss).selected_index
		elm.pbYume = 1 if idx >= 1 else 0
		
		# 天冥値
		idx = self.GetUI(UIKind.SegCon_up).selected_index
		elm.tenmei = idx
		assert (0 <= idx and idx <= 2)
		
		# 白鍵
		idx = self.GetUI(UIKind.SegCon_wKey).selected_index
		elm.wKey   = 1 if idx >= 1 else 0
		
		#print(elm.dID, elm.a2Rare, elm.a2Yume, elm.a3Rare, elm.a3Yume, elm.pbYume, elm.tenmei, elm.wKey)
		self.data.AddElem(elm)
		
		self.UpdateSum(self.master)
		
		# 取り消しボタンを有効化
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
	mainView = AnadanSum()

