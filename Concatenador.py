import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os


def get_relative_path(path):
    start = os.getcwd()
    return os.path.relpath(path, start)

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    im_list = [im for im in im_list if im is not None]  # Remove imagens nulas
    if not im_list:
        return None

    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def concat_images():
    file_paths = filedialog.askopenfilenames(title='Selecione imagens para concatenar', filetypes=[('Imagens', '*.jpg *.png *.jpeg *.bmp *.gif')])

    if not file_paths:
        return  # O usuário cancelou a seleção

    relative_file_paths = [get_relative_path(file_path) for file_path in file_paths]

    images = [cv2.imread(file_path.encode('utf-8').decode('unicode_escape')) for file_path in relative_file_paths]

    concatenated_image = vconcat_resize_min(images)

    if concatenated_image is not None:
        # Codifica a imagem em um formato de imagem padrão do Windows
        encoded_image = cv2.imencode('.jpg', concatenated_image)[1]

        # Decodifica a imagem e salva no formato desejado
        saved_image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
        cv2.imwrite('Compilado.jpg', saved_image)
        cv2.imshow('Imagem Concatenada', concatenated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

root = tk.Tk()
root.title('Concatenar Imagens')
root.geometry("300x300")  # Definindo a geometria da janela


concat_button = tk.Button(root, text='Concatenar Imagens', command=concat_images)
concat_button.pack()

concat_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
concat_button.config(bg='blue', fg='white', font=(12))

root.mainloop()
