# ==================================
# ガルレア周回のデータ蓄積 : 定義
# - 猫神神社や夢詠みの出現率を測る
# ==================================
# ----------------------------------
# import module
# ----------------------------------
from enum import IntEnum, auto
from collections import namedtuple

# --------------------------------
# 定義
# --------------------------------
# セーブするCSVファイル名
SaveCSV = 'ガルレア周回蓄積データ.csv'

# マスターデータ
tMaster = namedtuple('tMaster', 'dID, addable, name, banner, rareName')
Master = [
	tMaster(
		0, False, 
		'すべて', 'gbn00.PNG', 
		'レアエリア'
	),
	tMaster(
		1, True, 
		'現代ガルレア大陸', 'gbn01.PNG', 
		'猫神神社'
	),
	tMaster(
		2, True, 
		'古代ガルレア大陸', 'gbn02.PNG', 
		'土偶の秘境'
	),
]

# データのキー種別
class KeyKind(IntEnum):
	KK_Date		= auto()	# 登録日時
	KK_DID  	= auto()	# ダンジョンID	
	KK_A1_Jin	= auto()	# エリア1で猫神神社
	KK_A2_Jin	= auto()	# エリア2で猫神神社
	KK_A3_Jin	= auto()	# エリア3で猫神神社
	KK_Gyoku	= auto()	# 攻撃の硬玉の個数
	KK_Yume 	= auto()	# 夢詠みの書の個数
	KK_TenMei	= auto()	# 天冥値が上がったか
	KK_WKey		= auto()	# 白鍵が出たか

# データのキー文字列
KeyStr = {
	KeyKind.KK_Date		: 'Date',
	KeyKind.KK_DID 		: 'DID',
	KeyKind.KK_A1_Jin   : 'A1Jin',
	KeyKind.KK_A2_Jin   : 'A2Jin',
	KeyKind.KK_A3_Jin   : 'A3Jin',
	KeyKind.KK_Gyoku    : 'Gyoku',
	KeyKind.KK_Yume     : 'Yume',
	KeyKind.KK_TenMei 	: 'Tenmei',
	KeyKind.KK_WKey		: 'WKey',
}

