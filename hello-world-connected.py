import tecplot as tp

# connect to running instance of Tecplot 360 on the default port (7600)
tp.session.connect()

# reset the layout. This will clear any previously loaded data
tp.new_layout()

# get handle to the active frame
frame = tp.active_frame()

# add a text box. The anchor will be in the center of the frame
frame.add_text('Hello, World!', (50, 50))

