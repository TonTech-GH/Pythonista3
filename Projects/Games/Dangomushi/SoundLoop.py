import ui
import sound
import threading

# ループさせるビート
BGM = 'sound/loop/Break 02.mp3'

# ループ間隔
LoopTime = 2.38


'''
メイン処理
'''
if __name__ == '__main__':
	#ビュー	
	v = ui.View()
	v.present('fullscreen')
	v.background_color = .77, .97, 1.0
	
	#テキスト表示
	t = ui.TextView()
	t.frame = (0,v.height*.3, v.width, v.height*.3)
	t.alignment = ui.ALIGN_CENTER
	t.editable = False
	v.add_subview(t)
	
	#ボタン
	btn = ui.Button()
	btn.title = 'play'
	btn.background_color = 1.0, .84, .62
	btn.frame = (0,0,v.width, v.height*.2)
	btn.t = t
	v.add_subview(btn)
	btn.stop = False
	
	#ボタンタップアクション
	def Tapped(btn):
		btn.stop = True
	btn.action = Tapped
	
	#タイマー実行される処理
	def task(): 
		if btn.stop:
			return 
		
		#サウンド
		snd = sound.play_effect(BGM)
		
		# 繰り返し予約
		t=threading.Timer(LoopTime, task)
		t.start()

	# 繰り返し処理の起点
	t=threading.Thread(target=task)
	t.start()
	
