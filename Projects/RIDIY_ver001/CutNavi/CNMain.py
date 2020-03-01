# ==================================
# カットナビゲーター : メイン
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
from CNData import CNData as CND
from CNView import CNView as CNV


# ----------------------------------
# カットナビゲーターのメイン
# ----------------------------------
class CNMain:
	def __init__(self):
		self.Setting()
	
	def Setting(self):
		self.d = CND()
		self.v = CNV(self.d)
	
# --------------------------------
# 単体テスト
# --------------------------------
if __name__ == '__main__':
	cnm = CNMain()

