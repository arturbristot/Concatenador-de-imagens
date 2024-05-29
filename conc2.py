import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

def get_relative_path(path):
    start = os.getcwd()
    return os.path.relpath(path, start)

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    im_list = [im for im in im_list if im is not None]
    if not im_list:
        return None

    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def concat_images_from_folder():
    try:
        group_size = int(images_per_group_entry.get())
        if group_size <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Insira um número inteiro positivo para imagens por compilado.")
        return

    folder_path = filedialog.askdirectory(title='Selecione a pasta com as imagens')
    if not folder_path:
        return

    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif'))
    ]

    image_groups = [image_files[i:i + group_size] for i in range(0, len(image_files), group_size)]

    for i, group in enumerate(image_groups):
        images = [cv2.imread(file_path) for file_path in group]
        concatenated_image = vconcat_resize_min(images)

        if concatenated_image is not None:
            cv2.imwrite(f'Compilado_{i + 1}.jpg', concatenated_image)

    cv2.destroyAllWindows()
    messagebox.showinfo("Concluído", f"Imagens concatenadas em grupos de {group_size} salvas na pasta atual.")

root = tk.Tk()
root.title('Concatenar Imagens')
root.geometry("220x200")  # Aumenta a largura da janela
root.configure(bg="#f0f0f0")  # Cor de fundo clara

# Estilo para os elementos
style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Roboto", 12))
style.configure("TEntry", font=("Roboto", 12))
style.configure("TButton", background="#333", foreground="black", 
                font=("Roboto", 12, "bold"), padding=10)

frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

images_per_group_label = ttk.Label(frame, text="Imagens por compilado:")
images_per_group_label.grid(row=0, column=0, sticky="w")

images_per_group_entry = ttk.Entry(frame)
images_per_group_entry.grid(row=1, column=0, pady=10, sticky="ew")
images_per_group_entry.insert(0, "12") 

concat_button = ttk.Button(frame, text='Concatenar Imagens', command=concat_images_from_folder)
concat_button.grid(row=2, column=0, sticky="ew")

root.mainloop()