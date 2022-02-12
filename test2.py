import tkinter as tk
import tkinter.font as tkf

root = tk.Tk()

def check(ev):
    root.update()
    but['state'] = 'disabled' if not en.get() else 'normal'
en = tk.Entry(root)

but = tk.Button(root, text='y')



en.pack()
but.pack()
root.bind('<Key>', check)

root.mainloop()