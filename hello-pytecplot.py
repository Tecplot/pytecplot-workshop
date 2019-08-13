import tecplot as tp

# connect to running instance of Tecplot 360 on port 7601
tp.session.connect(port=7601)

# reset the layout. This will clear any previously loaded data
tp.new_layout()

# get handle to the active frame
frame = tp.active_frame()

# add a text box. The anchor will be in the center of the frame
txt = frame.add_text('Hello, PyTecplot!', (50, 50))

# make text larger
txt.size = 48

# center text by centering the anchor point
txt.anchor = TextAnchor.MidCenter

# change the text color
txt.color = Color.Blue

