import tecplot as tp

# get handle to the active frame
frame = tp.active_frame()

# add a text box. The anchor will be in the center of the frame
frame.add_text('Hello, World!', (50, 50), size=48)

# save an image of the frame
tp.save_png('hello-world.png')

