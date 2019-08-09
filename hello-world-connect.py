import tecplot as tp
tp.session.connect()
tp.new_layout()
frame = tp.active_frame()
frame.add_text('Hello, World!', (50, 50))
