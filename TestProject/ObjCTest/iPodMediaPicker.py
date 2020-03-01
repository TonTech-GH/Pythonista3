# iPodライブラリのメディアを取得

import ui
# Objective C ブリッジ
from objc_util import *

# メディアピッカークラスの取得
pClass = ObjCClass('MPMediaPickerController')
print(pClass)

# メディアピッカーのインスタンス生成
picker = pClass.alloc()
print(picker)

#type = MPMediaTypeAnyAudio
picker.init()


v = ui.View()
v.background_color = '#b1ddff'
v.present('fullscreen')

