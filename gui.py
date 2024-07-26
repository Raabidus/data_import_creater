import tkinter as tk
from tkinter import ttk


# window
window = tk.Tk()
window.title('Importer test gui')
window.geometry('500x350')

# title
title_label = ttk.Label(master = window, text = 'test')
title_label.pack()

# run window
window.mainloop()