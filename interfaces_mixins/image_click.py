import tkinter as tk
from PIL import Image, ImageTk


def on_click(event=None):
    # `command=` chama a função sem argumento
    # `bind` chama uma função com pelo menos um argumento
    print("image clicked")


# --- main ---

root = tk.Tk()

# Carrega a imagem
teste = Image.open('../src/espaco_inventario.png')
photo = ImageTk.PhotoImage(teste)

# Label com imagem
l = tk.Label(root, image=photo)
l.pack()

# Bind sendo atribuido a função on_click
l.bind('<Button-1>', on_click)

# Botão com o mesmo bind so que no command
b = tk.Button(root, image=photo, command=on_click)
b.pack()

# Botão para fechar a janela
b = tk.Button(root, text="Close", command=root.destroy)
b.pack()

root.mainloop()