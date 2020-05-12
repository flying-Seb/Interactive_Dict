'''
This is going to be the graphical user interface for the interactive dictionary - developed with tkinter
'''

# some tests

from tkinter import *

window = Tk(className="Interactive Dictionary")

for i in range(3):
    window.rowconfigure(i, weight=1, minsize=50)
    window.columnconfigure(i, weight=1, minsize=75)

    for j in range(3):
        frame_a = Frame(
            master=window,
            relief=RAISED,
            borderwidth=1,
        )
        frame_a.grid(row=i, column=j, padx=5, pady=5)

        lbl_a = Label(master=frame_a, text=f"Row: {i}, Column: {j}")
        lbl_a.pack(padx=5, pady=5)


window.mainloop()
