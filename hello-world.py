import tecplot as tp
tp.new_layout()
frame = tp.active_frame()
frame.add_text('Hello, World!', (50, 50))
tp.save_png('hello-world.png')
