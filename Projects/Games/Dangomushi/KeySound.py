import ui
import sound
from collections import namedtuple

# 音階
KeyConf = namedtuple('MKey', 'name, file')
MKey = {
	'ド2'   : KeyConf('ド', 'sound/key/Key_C2.mp3'),
	'レ2'   : KeyConf('レ', 'sound/key/Key_D2.mp3'),
	'ミ2'   : KeyConf('ミ', 'sound/key/Key_E2.mp3'),
	'ファ2' : KeyConf('ﾌｧ', 'sound/key/Key_F2.mp3'),
	'ソ2'   : KeyConf('ソ', 'sound/key/Key_G2.mp3'),
	'ラ2'   : KeyConf('ラ', 'sound/key/Key_A2.mp3'),
	'シ2'   : KeyConf('シ', 'sound/key/Key_B2.mp3'),
	'ド3'   : KeyConf('ド', 'sound/key/Key_C3.mp3'),
	'レ3'   : KeyConf('レ', 'sound/key/Key_D3.mp3'),
	'ミ3'   : KeyConf('ミ', 'sound/key/Key_E3.mp3'),
	'ファ3' : KeyConf('ﾌｧ', 'sound/key/Key_F3.mp3'),
	'ソ3'   : KeyConf('ソ', 'sound/key/Key_G3.mp3'),
	'ラ3'   : KeyConf('ラ', 'sound/key/Key_A3.mp3'),
	'シ3'   : KeyConf('シ', 'sound/key/Key_B3.mp3'),
	'ド4'  : KeyConf('ド', 'sound/key/Key_C4.mp3'),
	'レ4'  : KeyConf('レ', 'sound/key/Key_D4.mp3'),
	'ミ4'  : KeyConf('ミ', 'sound/key/Key_E4.mp3'),
	'ファ4': KeyConf('ﾌｧ', 'sound/key/Key_F4.mp3'),
	'ソ4'  : KeyConf('ソ', 'sound/key/Key_G4.mp3'),
}

'''
メイン処理
'''
if __name__ == '__main__':
	def UpdateText(t, idx):
		for i,(key,val) in enumerate(MKey.items()):
			if i == idx:
				t.text = key + '\n' + val.name + '\n' + val.file
		
	def PlaySound(b):
		idx = b.idx
		for i,(key,val) in enumerate(MKey.items()):
			if i == idx:
				sound.play_effect(val.file)
				break
			
		idx += 1
		if idx >= len(MKey): idx = 0
		b.idx = idx
		UpdateText(b.t, idx)
	
	
	v = ui.View()
	v.background_color = .81, .97, 1.0
	v.present('fullscreen')
	
	b = ui.Button()
	b.idx = 0
	b.action = PlaySound
	b.title = 'Play Sound'
	b.width = v.width / 2
	b.height = v.height / 3
	b.center = (v.width / 2, b.height / 2 + 20)
	b.border_width = 2
	b.border_color = .0, .0, .0
	b.background_color = 1.0, .95, .62
	v.add_subview(b)
	
	t = ui.TextView()
	t.text = 'Key'
	t.alignment = ui.ALIGN_CENTER
	t.font = '<System-Bold>', 20
	t.editable = False
	t.width = b.width
	t.height = v.height / 3
	t.center = (v.width / 2, v.height / 2 + t.height / 2)
	UpdateText(t, b.idx)
	v.add_subview(t)
	b.t = t
