# Importação das bibliotecas necessárias
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# Função para obter o caminho relativo de um arquivo
def get_relative_path(path):
    start = os.getcwd()
    return os.path.relpath(path, start)

# Função para concatenar imagens verticalmente com redimensionamento
def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    im_list = [im for im in im_list if im is not None] 
    if not im_list:
        return None

    # Encontre a largura mínima entre as imagens
    w_min = min(im.shape[1] for im in im_list)
    
    # Redimensione todas as imagens para ter a mesma largura
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1]), interpolation=interpolation) for im in im_list]
    
    return cv2.vconcat(im_list_resize)

# Função para a concatenação de imagens
def concat_images():
    # Abra a janela de diálogo para selecionar várias imagens
    file_paths = filedialog.askopenfilenames(title='Selecione imagens para concatenar', filetypes=[('Imagens', '*.jpg *.png *.jpeg *.bmp *.gif')])

    if not file_paths:
        return 

    # Converta os caminhos absolutos das imagens em caminhos relativos
    relative_file_paths = [get_relative_path(file_path) for file_path in file_paths]

    # Carregue as imagens usando OpenCV
    images = [cv2.imread(file_path.encode('utf-8').decode('unicode_escape')) for file_path in relative_file_paths]

    # Concatene as imagens verticalmente
    concatenated_image = vconcat_resize_min(images)

    if concatenated_image is not None:
        # Codifique a imagem resultante em formato JPEG
        encoded_image = cv2.imencode('.jpg', concatenated_image)[1]

        # Decodifique a imagem para exibição
        saved_image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)

        # Salve a imagem concatenada em um arquivo
        cv2.imwrite('Compilado.jpg', saved_image)

        # Exiba a imagem resultante em uma janela
        cv2.imshow('Imagem Concatenada', concatenated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Crie a janela principal da interface gráfica
root = tk.Tk()
root.title('Concatenar Imagens')
root.geometry("300x300")  

# Crie um botão na interface gráfica para iniciar o processo de concatenação
concat_button = tk.Button(root, text='Concatenar Imagens', command=concat_images)
concat_button.pack()

# Posicione o botão no centro da janela
concat_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Configure o estilo do botão
concat_button.config(bg='blue', fg='white', font=(12))

# Inicie a interface gráfica
root.mainloop()
