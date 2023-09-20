import tkinter as tk
import os
# r = tk.Tk()
# r.title("refresh button")
# def refresh():
#     r.destroy()
#     os.popen("teste.py") #change refresh.py according to yours program name
# button_1 = tk.Button(r,text = "Refresh",command = refresh)
# button_1.pack()
# def exit():
#     r.destroy()
# button_2 = tk.Button(r,text = "Exit",command = exit)
# button_2.pack()
# r.mainloop()

my_file = open("../banco_de_dados/historico_1.txt", "r")
content = my_file.read()
content_list = content.split("\n")
my_file.close()
print(content_list)