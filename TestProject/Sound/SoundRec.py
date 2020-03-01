import ui
import sound
from datetime import datetime # 現在時刻取得

'''
保存ファイル名の取得
'''
def SevedFName():
	name = 'rec_'
	# 現在時刻をくっつける
	time = datetime.now()
	timeStr = time.strftime('%Y%m%d_%H%M')
	return name + timeStr + '.m4a'

'''
録音終了
'''
def StopRec(btn):
	btn.rec.stop()
	btn.title = 'Stoped'
	btn.action = None

'''
録音開始
'''
def StartRec(btn):
	rec = sound.Recorder(SevedFName())
	rec.record(10)
	btn.rec = rec
	btn.title = 'stop'
	btn.action = StopRec


'''
メイン処理
'''
if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
	
	btn = v['btnRec']
	btn.action = StartRec
	


