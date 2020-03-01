# ==================================
# アナダン周回のデータ蓄積 : 定義
# - レアエリアや夢詠みの出現率を測る
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
SaveCSV = 'アナダン周回蓄積データ.csv'

#マスターデータ
tMaster = namedtuple('tMaster', 'dID, addable, name, banner, a2n, a2r, a3n, a3r')
Master = [
	tMaster(
		0, False,
		'すべて', 'bn00.PNG',
		'通常', 'レア',
		'通常', 'レア',
	),
	tMaster(
		1, True,
		'ミグランス城', 'bn01.PNG',
		'側塔', '門塔',
		'別棟', '門衛棟',
	),
	tMaster(
		2, True,
		'工業都市廃墟', 'bn02.PNG',
		'炉内'   , '炉内警戒区',
		'エリアC', 'エリアR',
	),
	tMaster(
		3, True,
		'月影の森', 'bn03.PNG',
		'獣道'   , '茨道',
		'自然歩道', '神秘歩道',
	),
	tMaster(
		4, True,
		'魔獣城', 'bn04.PNG',
		'監視塔', '胸壁付監視塔',
		'主塔'  , '主塔内貯蔵庫',
	),
	tMaster(
		5, True,
		'蛇肝ダマク', 'bn05.PNG',
		'小網部'   , '幽門',
		'腹腔部'   , '噴門',
	),
	tMaster(
		6, True,
		'ゼノドメイン', 'bn06.PNG',
		'工業セクター', '加工セクター',
		'研究区'     , '機密研究区',
	),
]

# データのキー種別
class KeyKind(IntEnum):
	KK_Date			= auto()	# 登録日時
	KK_DID  		= auto()	# ダンジョンID	
	KK_A2_Rare	= auto()	# エリア2はレアエリアか
	KK_A2_Yume	= auto()	# エリア2で夢詠みが出たか
	KK_A3_Rare	= auto()	# エリア3はレアエリアか
	KK_A3_Yume	= auto()	# エリア3で夢詠みが出たか
	KK_PB_Yume	= auto()	# ボス前宝箱から夢詠みが出たか
	KK_TenMei		= auto()	# 天冥値が上がったか
	KK_WKey			= auto()	# 白鍵が出たか

# データのキー文字列
KeyStr = {
	KeyKind.KK_Date			: 'Date',
	KeyKind.KK_DID 			: 'DID',
	KeyKind.KK_A2_Rare  : 'A2Rare',
	KeyKind.KK_A2_Yume  : 'A2Yume',
	KeyKind.KK_A3_Rare  : 'A3Rare',
	KeyKind.KK_A3_Yume  : 'A3Yume',
	KeyKind.KK_PB_Yume  : 'PBYume',
	KeyKind.KK_TenMei 	: 'Tenmei',
	KeyKind.KK_WKey			: 'WKey',
}

