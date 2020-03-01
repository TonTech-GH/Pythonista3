# ==================================
# カットナビゲーター : 定義
# - 木材カットの良い取回しを提案する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
from enum import IntEnum, auto

# ----------------------------------
# 定数
# ----------------------------------
# カットのマージン(mm)
CUT_MARGIN = 10

# ----------------------------------
# 素材種別
# ----------------------------------
class Kind (IntEnum):
	EK_None= 0
	EK_1x4 = auto()
	EK_2x4 = auto()
	EK_1x1 = auto()
	EK_1x2 = auto()
	EK_1x3 = auto()
	EK_1x6 = auto()
	EK_1x8 = auto()
	EK_1x10= auto()
	EK_2x1 = auto()
	EK_2x2 = auto()
	EK_2x3 = auto()
	EK_2x6 = auto()

# 各素材種別の表示文字列
KindStr = {
	Kind.EK_1x4 : '1x4',
	Kind.EK_2x4 : '2x4',
	Kind.EK_1x1 : '1x1',
	Kind.EK_1x2 : '1x2',
	Kind.EK_1x3 : '1x3',
	Kind.EK_1x6 : '1x6',
	Kind.EK_1x8 : '1x8',
	Kind.EK_1x10: '1x10',
	Kind.EK_2x1 : '2x1',
	Kind.EK_2x2 : '2x2',
	Kind.EK_2x3 : '2x3',
	Kind.EK_2x6 : '2x6',
}

# ----------------------------------
# 長さ
# ----------------------------------
class Len (IntEnum):
	Len_3F =  914	# 3フィート
	Len_6F = 1829	# 6フィート
	
# ----------------------------------
# 必要素材
# ----------------------------------
class Elem:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# 素材種別
		self.kind = Kind.EK_None
		
		# 長さ
		self.len = 0
		
		# 本数
		self.num = 0	

# ----------------------------------
# 用意すべき材料
# ----------------------------------
class Material:
	# ----------------------------------
	# コンストラクタ
	# ----------------------------------
	def __init__(self):
		# 素材種別
		self.kind = Kind.EK_None
		
		# 長さ
		self.len = Len.Len_6F
		
		# 取る長さリスト(Cut List)
		self.cls = []
	
	# ----------------------------------
	# 合計長さの取得(マージン含む)
	# ----------------------------------
	def TtlLen(self):
		ttl = sum(self.cls)
		if ttl <= 0:
			return 0
		
		# マージンの追加
		for i in range(0, len(self.cls)):
			ttl += CUT_MARGIN
		
		assert ttl <= self.len, '長さオーバーしている'
		return ttl
	
	# ----------------------------------
	# 追加できるか
	# ----------------------------------
	def Addable(self, l:int):
		if l <= 0:	return False
		
		# 現在の合計長さ
		ttl = self.TtlLen()
		
		# 追加後の合計長さ
		if ttl == 0: ttl = CUT_MARGIN
		added = ttl + l + CUT_MARGIN
		
		if added <= self.len:
			return True
		return False
	
	# ----------------------------------
	# 追加する
	# ----------------------------------
	def Add(self, l:int):
		assert self.Addable(l), str(l) + 'は追加不可'
		self.cls.append(l)
			
	
	# ----------------------------------
	# 最適化結果の出力
	# ----------------------------------
	def Output(self):
		res = self
		if not(res): 
			print(res) 
			return 
		print('\n=== Proposal Result ===')
		print('kind : ', res.kind)
		print('Len  : ', res.len)
		print('CLS  : ', res.cls)
