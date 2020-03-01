# 再生中の曲情報を取得、出力
# デフォルトのミュージックアプリの再生曲のみ取得可

# Objective C ブリッジ
from objc_util import *

# ミュージックプレイヤークラス取得
MPMusicPlayerController = ObjCClass('MPMusicPlayerController')

# ミュージックプレイヤーの取得
player = MPMusicPlayerController.systemMusicPlayer()

# 再生中の曲情報取得
now_playing = player.nowPlayingItem()
if now_playing:
	artist = now_playing.valueForProperty_('artist')
	title = now_playing.valueForProperty_('title')
	print('Now playing: %s -- %s' % (artist, title))
else:
	print('No music playing')
