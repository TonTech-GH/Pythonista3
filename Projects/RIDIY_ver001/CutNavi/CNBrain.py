# ==================================
# カットナビゲーター : 頭脳
# - 木材カットの良い取回しを提案する
# ==================================
# ----------------------------------
# import module
# ----------------------------------
import os, sys
from os import path
TheDir = path.dirname(path.abspath(__file__))
if (TheDir in sys.path) == False:
	sys.path.append(TheDir)
from CNDef import *
from enum import IntEnum, auto

# 数理最適化ソルバー
# 内部でC言語のライブラリを使うのでPythonistaでは使えない
#from ortoolpy import binpacking

# ----------------------------------
# 定義
# ----------------------------------
# 最適化手法
class OptiWay(IntEnum):
	No   = auto()	# 最適化しない
	PuLP = auto()	# PuLPを使う
	Mine = auto()	# 自力でなんとかする
# 使用する最適化手法
OPTI_WITH = OptiWay.Mine

# デバッグ出力するか
DEBUG_OUT = __name__ == '__main__'

# --------------------------------
# 取回しの提案(最適化)
# --------------------------------
def Optimize(elms):
	# 入力を1次元リストにまとめる
	lenLs = []
	for elm in elms:
		for i in range(0, elm.num):
			lenLs.append(elm.len)
	
	# 最適化
	if OPTI_WITH == OptiWay.No:
		return NoOptimize(lenLs)
	elif OPTI_WITH == OptiWay.Mine:
		return MyOptimize(lenLs)
	
	assert False, str(OPTI_WITH) + 'は現在未対応'

# --------------------------------
# 最適化せず適当に並べる
# --------------------------------
def NoOptimize(lenLs):
	retLs = []
	# 必要素材リストが無くなるまで結果に登録していく
	while len(lenLs) > 0:
		mtl = Material()
		margin = CUT_MARGIN
		for l in lenLs[:]:
			assert l + CUT_MARGIN * 2 < Len.Len_6F, str(l) + ' is too oong'
			if mtl.TtlLen() + margin + l > Len.Len_6F:
				continue
			mtl.cls.append(l)
			margin += CUT_MARGIN
			lenLs.remove(l)
		retLs.append(mtl)
	return retLs

# --------------------------------
# 自力で最適化
# --------------------------------
def MyOptimize(lenLs:list):
	retLs = []
	
	# 入力データ
	if DEBUG_OUT:
		print('\n=== 元の必要素材リスト ===')
		print(lenLs)
	
	# 降順ソート
	lenLs.sort(reverse=True)
	if DEBUG_OUT:
		print('\n=== 降順にソートした必要素材リスト ===')
		print(lenLs)
	
	# 最悪値(=必要素材数)分の結果格納要素リスト
	tmpMtl = []
	for i in range(0, len(lenLs)):
		tmpMtl.append(Material())
		
	# 先頭から順に詰めていく
	idx = 0
	for l in lenLs:
		added = False
		for i in range(0, idx):
			if tmpMtl[i].Addable(l):
				tmpMtl[i].Add(l)
				added = True
				break
		
		if added == False:
			tmpMtl[idx].Add(l)
			idx += 1
	
	# 長さが入っているのだけ抽出
	for i in range(0, len(tmpMtl)):
		if tmpMtl[i].TtlLen() > 0:
			retLs.append(tmpMtl[i])
	
	return retLs
	
# --------------------------------
# 最低必要本数を算出
# --------------------------------
def MinNum(elms):
	ttl = CUT_MARGIN
	for e in elms:
		e:Elem
		if e.len <= 0:
			continue
		ttl += (e.len + CUT_MARGIN) * e.num
	print('Total Length : ', ttl)
	
	num = 0
	if ttl > CUT_MARGIN:
		len = Len.Len_6F
		num = (ttl - 1) / len + 1
		num = int(num)
	print('Min Num : ', num)
	return num
	

# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	'''
	min =  100 #Len.Len_6F - 50
	max = 1800 #Len.Len_6F - 30
	elms = []
	for i in range(min, max, 100):
		elm = Elem()
		elm.len = i
		elm.num = 1
		elms.append(elm)
	'''
	
	elms = []
	for i in range(0, 4):
		elm = Elem()
		elm.kind = Kind.EK_1x4
		elm.num  = 4
		elms.append(elm)
	
	elms[0].len = 320
	elms[1].len = 403
	elms[2].len = 248
	elms[3].len = 123
	elms[3].num = 1
	
	retLs = Optimize(elms)
	for mtl in retLs:
		mtl.Output()
