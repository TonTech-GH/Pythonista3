import ui

v = ui.load_view()
v.present('sheet')

# スクロールビュー
sv = v['scrollview1']
#sv = ui.ScrollView()
#sv.content_offset = (-20, -20)
#sv.content_inset = (20, 20, 100, 100)

for i in range(0, 15):
	for k in range(0,5):
		btn = ui.Button()
		btn.frame = (40*k, 30 * i, 40, 20)
		btn.background_color = '#099fff'
		btn.border_width = 1
		btn.border_color = '#000000'
		btn.title = str(i+1) + '-' + str(k+1)
		
		sv.add_subview(btn)

