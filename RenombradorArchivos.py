import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

# Función para seleccionar carpeta
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        # Verificar si la carpeta está vacía
        archivos = os.listdir(carpeta)
        if not archivos:
            messagebox.showwarning("Advertencia", "La carpeta seleccionada está vacía. No hay archivos para renombrar.")
            return
        
        while True:  # Bucle para solicitar el nombre base hasta que sea válido
            nuevo_nombre_base = simpledialog.askstring("Entrada de nombre", "Ingrese el nombre base para los archivos:")
            
            if nuevo_nombre_base is None:  # Si el usuario cierra el diálogo
                return
            
            if nuevo_nombre_base.strip() == "":
                messagebox.showwarning("Advertencia", "El nombre base no puede estar vacío.")
            else:
                break  # Salir del bucle si el nombre es válido

        abrir_seleccionador_separador(carpeta, nuevo_nombre_base)

# Función para abrir ventana de selección de separador
def abrir_seleccionador_separador(carpeta, nuevo_nombre_base):
    ventana_separador = tk.Toplevel(root)
    ventana_separador.title("Seleccionar Separador")
    ventana_separador.geometry("250x200")
    ventana_separador.minsize(250, 200)

    # Crear un Canvas en la ventana secundaria para el fondo
    canvas_separador = tk.Canvas(ventana_separador, width=300, height=200)
    canvas_separador.pack(fill="both", expand=True)

    # Establecer un fondo sólido azul claro
    canvas_separador.configure(bg="#87CEEB")

    def seleccionar_espacio():
        cambiar_nombres(carpeta, nuevo_nombre_base, " ")
        ventana_separador.destroy()

    def seleccionar_guion_bajo():
        cambiar_nombres(carpeta, nuevo_nombre_base, "_")
        ventana_separador.destroy()

    def cancelar():
        ventana_separador.destroy()

    # Crear botones y colocarlos en el canvas
    btn_espacio = tk.Button(ventana_separador, text="Espacio", command=seleccionar_espacio, bg="#F5F5DC")
    btn_guion_bajo = tk.Button(ventana_separador, text="Guion Bajo", command=seleccionar_guion_bajo, bg="#F5F5DC")
    btn_cancelar = tk.Button(ventana_separador, text="Cancelar", command=cancelar, bg="#F5F5DC")

    # Colocar los botones en el canvas
    btn_espacio_window = canvas_separador.create_window(125, 80, window=btn_espacio)
    btn_guion_bajo_window = canvas_separador.create_window(125, 120, window=btn_guion_bajo)
    btn_cancelar_window = canvas_separador.create_window(220, 170, window=btn_cancelar)

    # Función para centrar los botones de espacio y guion bajo
    def center_buttons(event):
        ancho_canvas = canvas_separador.winfo_width()
        canvas_separador.coords(btn_espacio_window, ancho_canvas / 2, 80)
        canvas_separador.coords(btn_guion_bajo_window, ancho_canvas / 2, 120)
        # Mantener "Cancelar" en la parte inferior derecha
        canvas_separador.coords(btn_cancelar_window, ancho_canvas - 70, event.height - 30)

    # Vincular el evento <Configure> para centrar los botones y mantener "Cancelar" en la parte inferior derecha
    canvas_separador.bind("<Configure>", center_buttons)

# Función para cambiar los nombres de los archivos
def cambiar_nombres(carpeta, nuevo_nombre_base, separador):
    archivos = os.listdir(carpeta)

    # Verificar si la carpeta está vacía
    if not archivos:
        messagebox.showwarning("Advertencia", "La carpeta está vacía. No hay archivos para renombrar.")
        return

    cont = 1
    for archivo in archivos:
        nombre_viejo = os.path.join(carpeta, archivo)
        extension = os.path.splitext(archivo)[1].lower()

        nombre_nuevo = os.path.join(carpeta, f"{nuevo_nombre_base}{separador}{cont}{extension}")

        if os.path.exists(nombre_nuevo):
            respuesta = messagebox.askyesno("Confirmación", f"El archivo {nombre_nuevo} ya existe. ¿Desea sobrescribirlo?")
            if not respuesta:
                cont += 1
                continue  # No sobrescribir, pasar al siguiente archivo

        try:
            os.rename(nombre_viejo, nombre_nuevo)
            cont += 1
        except OSError as e:
            messagebox.showerror("Error", f"No se pudo renombrar el archivo {archivo}. Detalle del error: {e}")

    messagebox.showinfo("Proceso completado", "¡Nombre(s) de archivo(s) cambiado(s) con éxito!")

# Función para crear el degradado
def crear_degradado(canvas, color_inicio, color_fin):
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    pasos = 100

    r1, g1, b1 = canvas.winfo_rgb(color_inicio)
    r2, g2, b2 = canvas.winfo_rgb(color_fin)
    r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
    r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256

    for i in range(pasos):
        r = int(r1 + (r2 - r1) * i / pasos)
        g = int(g1 + (g2 - g1) * i / pasos)
        b = int(b1 + (b2 - b1) * i / pasos)
        color = f"#{r:02x}{g:02x}{b:02x}"

        y1 = int(i * alto / pasos)
        y2 = int((i + 1) * alto / pasos)
        canvas.create_rectangle(0, y1, ancho, y2, outline="", fill=color)

# Función para centrar el botón
def center_btn():
    canvas.update_idletasks()
    ancho_canvas = canvas.winfo_width()
    alto_canvas = canvas.winfo_height()

    # Posicionar el botón en el centro
    canvas.coords(boton_id, ancho_canvas / 2, alto_canvas / 2)

# Función que combina el degradado y centrado del botón
def on_configure(event):
    # Crear el degradado y centrar el botón
    crear_degradado(canvas, "#0000FF", "#87CEEB")
    center_btn()

# Crear ventana principal
root = tk.Tk()
root.title("Programa Beta para renombrar archivos.")
root.geometry("350x400")
root.minsize(350, 400)

# Crear el widget Canvas
canvas = tk.Canvas(root, width=500, height=300)
canvas.pack(fill="both", expand=True)

# Vincular el evento <Configure> para redibujar el degradado y centrar el botón
canvas.bind("<Configure>", on_configure)

# Opciones del "logo"
try:
    img_logo = Image.open("cambiador_nobres_archivos(cna)(py)/img/logo.png")
    img_logo = img_logo.resize((40, 40), Image.LANCZOS)
    img_logo_tk = ImageTk.PhotoImage(img_logo)
    label_logo = tk.Label(canvas, image=img_logo_tk, bg="blue")
    label_logo.place(x=10, y=10)

    # Título al lado del logo
    label_titulo = tk.Label(canvas, text="Renombrador de archivos", font=("Arial", 14), bg="blue", fg="black")
    label_titulo.place(x=60, y=15)
except FileNotFoundError:
    messagebox.showerror("Error", "Imagen del logo no encontrada.")

# Opciones del icono "carpeta"
try:
    icon_folder = Image.open("cambiador_nobres_archivos(cna)(py)/img/folder.png")
    icon_folder = icon_folder.resize((30, 30), Image.LANCZOS)
    icon_folder_tk = ImageTk.PhotoImage(icon_folder)
    
    # Crear el botón con el ícono a la izquierda y texto a la derecha
    btn_seleccionar = tk.Button(
        root,
        text="Seleccionar carpeta",
        image=icon_folder_tk,
        compound="top",
        command=seleccionar_carpeta,
        bg="#F5F5DC",
        fg="black",
        padx=10,  
        pady=5     
    )
except FileNotFoundError:
    messagebox.showerror("Error", "Imagen del ícono de carpeta no encontrada.")
    btn_seleccionar = tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta)

# Colocar el botón dentro del canvas
boton_id = canvas.create_window(250, 150, window=btn_seleccionar)

root.mainloop()
