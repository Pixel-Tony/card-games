# import tkinter as tk

# root = tk.Tk()
# root.geometry('1400x900+200+50')






# class TestFrame:
#     __coords = {}
#     def __init__(self, root: tk.Tk, o, f) -> None:
#         self.name = 'aboba'
#         self.bankroll = 200

#         self.frame = tk.Frame(root,
#             bg='white',
#             highlightbackground='white',
#             highlightthickness=2)

#         self.e = dict()

#         self.frame.place(x=o*162, y=0, width=161, height=151)
#         self.name_label = tk.Label(self.frame, text=self.name, bg='white')
#         self.name_label.place(x=2, y=2, bordermode='outside', width=161-4)

#     def abobus(self, ev):
#         self.frame.configure(highlightbackground=
#             ['red', 'white'][self.frame['highlightbackground'] == 'red'])

#     def cards(self):

#         for i in range(4):
#             c = tk.PhotoImage(master=self.frame, file=f'./gfx/cards/{i}.png')
#             cl = tk.Label(image=c)
#             self.e[cl] = c
#             cl.place(x=0 + (81 // (4 - 1))*i, y=22, width=80, height=130)


# fr = TestFrame(root, 0, 4)
# fr.cards()
# f2 = TestFrame(root, 1, 2)
# root.bind("<Button-1>", fr.abobus)
# root.mainloop()
