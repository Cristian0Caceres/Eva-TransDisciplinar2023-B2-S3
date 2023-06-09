#------------------------------------------------------------------------------------------------------------------------
#importacion de librerias las cuales se usaran durante el programa
#------------------------------------------------------------------------------------------------------------------------

import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


#------------------------------------------------------------------------------------------------------------------------
#creacion de funcion la cual calcula todo dentro del plano inclinado 
#------------------------------------------------------------------------------------------------------------------------
def calcular_aceleracion(angulo, masa, coeficiente_roce=0):
    g = 9.8#definicion de la gravedad como 9.8 la cual corresponde a la gravedad de la tierra
    peso = masa * g
    radianes = (angulo * math.pi) / 180
    seno = math.sin(radianes)
    coseno = math.cos(radianes)
    pesox = seno * peso
    pesoy = coseno * peso

#-----------------------------------------------------------------------------------------------------
#Se especifican los limites del coeficiente de roce y el angulo, si se salen de esto, genere un error.
#-----------------------------------------------------------------------------------------------------

    if coeficiente_roce < 0 or coeficiente_roce > 1:
        raise ValueError("El coeficiente de roce debe estar entre 0 y 1")
    if angulo < 1 or angulo > 90:
        raise ValueError("El angulo debe estar entre 1 y 89 grados")
    
    N = pesoy#Se iguala el peso en Y con la fuerza normal.
    roce = round(N * coeficiente_roce, 2)
    fuerza_neta = round(pesox - roce, 2)# Calcular la fuerza neta (componente x del peso menos la fuerza de roce)
    fuerza_neta = max(fuerza_neta, 0)
    aceleracion = round(fuerza_neta / masa, 2)#Calcular la aceleración con roce.
    return aceleracion, round(masa, 2), angulo, roce, fuerza_neta, round(pesox, 2), round(pesoy, 2)#Se devueleven todos los datos por funcionalidad.


#------------------------------------------------------------------------------------------------------------------------
#Se crea una funcion en la cual se centrara en la visualizacion del triangulo rectangulo y la masa del plano inclinado.
#en conjunto a la debida modificacion del triangulo cada ves que se actualiza el anteriormente mencionado
#------------------------------------------------------------------------------------------------------------------------
def dibujar_triangulo(angulo):
    canvas.delete("triangulo")

    radianes = math.radians(angulo)#se calculan los radianes respecto al angulo ingresado por el usuario

    x1 = 40
    y1 = 450

    cateto_adyacente = 420
    cateto_opuesto = cateto_adyacente * math.tan(radianes)

    x2 = x1 + cateto_adyacente
    y2 = y1

    x3 = x1
    y3 = y1 - cateto_opuesto
    background_color = window.cget("bg")

    if angulo > 50: #cuando el angulo es mayor a 50 grados el triangulo se vuelve ""transparente"""
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill=background_color, tags="triangulo")
    else:
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill="lightblue", tags="triangulo")

    masa_size = 75
    masa_distance = 0.519 #Porcentaje de la hipotenusa donde se ubicará el cuadrado

    masa_x = x1 + cateto_adyacente * masa_distance - masa_size * 0.5
    masa_y = y1 - cateto_opuesto * masa_distance - masa_size 

   
    masa_angle = math.degrees(math.atan(cateto_opuesto / cateto_adyacente)) #Calcula el ángulo de inclinación de la masa

    cx = masa_x + masa_size / 2 #Rota la masa utilizando transformaciones de coordenadas
    cy = masa_y + masa_size / 2

    canvas.create_polygon( #creamos al triangulo rosa usando la variable canvas.create_polygon
        rotate_point(masa_x, masa_y, cx, cy, masa_angle),
        rotate_point(masa_x + masa_size, masa_y, cx, cy, masa_angle),
        rotate_point(masa_x + masa_size, masa_y + masa_size, cx, cy, masa_angle),
        rotate_point(masa_x, masa_y + masa_size, cx, cy, masa_angle),
        outline="black", fill="pink", tags="triangulo"
    )
def rotate_point(x, y, cx, cy, theta):
    #Aplica la fórmula de rotación a un punto
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))

    nx = (x - cx) * cos_theta - (y - cy) * sin_theta + cx
    ny = (x - cx) * sin_theta + (y - cy) * cos_theta + cy

    return nx, ny     


#------------------------------------------------------------------------------------------------------------------------
#Se crea una funcion que se centrara en la ventana de Tkinter en donde el usuario podra ingresar los datos.
#------------------------------------------------------------------------------------------------------------------------
def calcular_button_click():
    try:
        angulo = float(angulo_entry.get())
        masa = float(masa_entry.get())
        coeficiente_roce = float(coeficiente_roce_entry.get())

        aceleracion, masa_objeto, angulo_objeto, roce, fuerza_neta, pesox, pesoy = calcular_aceleracion(angulo, masa, coeficiente_roce)


        resultado_text.set(f"Aceleración: {aceleracion} m/s²\n"
                           f"Masa: {masa_objeto} kg \n"
                           f"Ángulo: {angulo_objeto} ° \n"
                           f"Fuerza de Roce = (N x μ) = {roce} N \n"
                           f"Fuerza Neta: P + N + Fr = {fuerza_neta} N \n"
                           f"Peso en X = P x sen(α) = {pesox} N \n"
                           f"Peso en Y = P x cos(α) = {pesoy} N ")
                           #Se escriben los reslutados con sus respectivas formulas del como se llegaron a estos.
        
        dibujar_triangulo(angulo)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

#------------------------------------------------------------------------------------------------------------------------
#definicion de la funcion de ventana de ayuda angulo la cual genera una ayuda para guiar al usuario
#------------------------------------------------------------------------------------------------------------------------
def abrir_ventana_ayuda_angulo():
    ventana_ayuda = tk.Toplevel(window)
    ventana_ayuda.title("¿Qué es el ángulo?")
    ventana_ayuda.geometry("450x350")  # Ajusta las dimensiones de la ventana según tus necesidades

    # Contenido textual
    titulo_label = tk.Label(ventana_ayuda, text="¿Qué representa el ángulo?", font=("Arial", 20, "bold"))
    titulo_label.pack()

    contenido_text = tk.Label(ventana_ayuda, justify="left", font=("Arial", 16))

    #Párrafo
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nLa función del angulo en el plano inclinado es determinar la facilidad")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ncon la cual el objeto se desliza por el plano (no es el unico que lo determina)")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nentre mayor sea el angulo, mas facil sera para el objeto deslizarce ")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ny entre menor sea, mas dificil se le hara, este angulo puede llegar a los 360 grados")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\npero en el caso del plano inclinado solo hasta los 90 grados")
    contenido_text.configure(text=contenido_text.cget("text") + "\n")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nEjemplo visual del como efecta el angulo a la masa:")
    
    contenido_text.pack()

    #Imagen
    imagen_path = "anguloplanoej1.png"  #Reemplaza con la ruta de tu imagen
    imagen = Image.open(imagen_path)
    imagen = imagen.resize((800, 300))  #Ajusta el tamaño de la imagen según tus necesidades
    imagen_tk = ImageTk.PhotoImage(imagen)
    imagen_label = tk.Label(ventana_ayuda, image=imagen_tk)
    imagen_label.image = imagen_tk  #Mantén una referencia a la imagen para evitar que sea eliminada por el recolector de basura
    imagen_label.pack()

    # Ajustar tamaño de la ventana al contenido
    ventana_ayuda.update_idletasks()
    ventana_ayuda.geometry(f"{ventana_ayuda.winfo_width()*2}x{ventana_ayuda.winfo_height()*2}")

#------------------------------------------------------------------------------------------------------------------------
#definicion de la funcion de ventana de ayuda masa(se repiten comentarios del angulo)
#------------------------------------------------------------------------------------------------------------------------
def abrir_ventana_ayuda_masa():
    ventana_ayuda = tk.Toplevel(window)
    ventana_ayuda.title("¿Qué es la masa?")
    ventana_ayuda.geometry("450x350")

   
    titulo_label = tk.Label(ventana_ayuda, text="¿Qué representa la masa?", font=("Arial", 20, "bold"))
    titulo_label.pack()

    contenido_text = tk.Label(ventana_ayuda, justify="left", font=("Arial", 16))

  
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nLa función de la masa en el plano inclinado es determinar la interaccion de gravedad en el peso y la aceleracion delntro del objeto")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ncon esto se determina como el objeto se desliza por el plano (no es el unico que lo determina)")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nentre mayor sea la masa, mas dificill sera para el objeto deslizarce ")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ny entre menor sea, mas facil se le hara")
    contenido_text.configure(text=contenido_text.cget("text") + "\n")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nEl Valor deve estar entre 0 a infinito positivo")
    
    contenido_text.pack()

 
    imagen_path = "peso-fisica.png"  
    imagen = Image.open(imagen_path)
    imagen = imagen.resize((800, 300))  
    imagen_tk = ImageTk.PhotoImage(imagen)
    imagen_label = tk.Label(ventana_ayuda, image=imagen_tk)
    imagen_label.image = imagen_tk  
    imagen_label.pack()

   
    ventana_ayuda.update_idletasks()
    ventana_ayuda.geometry(f"{ventana_ayuda.winfo_width()*2}x{ventana_ayuda.winfo_height()*2}")

#------------------------------------------------------------------------------------------------------------------------
#definicion de la funcion de ventana de ayuda coeficiente de roce(se repiten comentarios del angulo)
#------------------------------------------------------------------------------------------------------------------------
def abrir_ventana_ayuda_coeficiente_roce():
    ventana_ayuda = tk.Toplevel(window)
    ventana_ayuda.title("¿Qué es el coeficiente  de roce?")
    ventana_ayuda.geometry("450x350")


    titulo_label = tk.Label(ventana_ayuda, text="¿Qué representa el coeficiente de roce?", font=("Arial", 20, "bold"))
    titulo_label.pack()

    contenido_text = tk.Label(ventana_ayuda, justify="left", font=("Arial", 16))

    contenido_text.configure(text=contenido_text.cget("text") + "\n\nLa función del coeficiente de roce es la de determinar junto a la normal y la distancia")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ncomo  el objeto se desliza por el plano (no es el unico que lo determina) ")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nentre mayor sea el coeficiente de roce, seria mas dificil  para el objeto deslizarce ")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\ny entre menor sea, mas facil se le hara")
    contenido_text.configure(text=contenido_text.cget("text") + "\n")
    contenido_text.configure(text=contenido_text.cget("text") + "\n\nEl Valor deve estar entre 0 y 1 y ingresando los decimales con un . y no una ,")
    
    contenido_text.pack()

    imagen_path = "roce.jpg" 
    imagen = Image.open(imagen_path)
    imagen = imagen.resize((800, 300))
    imagen_tk = ImageTk.PhotoImage(imagen)
    imagen_label = tk.Label(ventana_ayuda, image=imagen_tk)
    imagen_label.image = imagen_tk
    imagen_label.pack()

    ventana_ayuda.update_idletasks()
    ventana_ayuda.geometry(f"{ventana_ayuda.winfo_width()*2}x{ventana_ayuda.winfo_height()*2}")

#------------------------------------------------------------------------------------------------------------------------
#funcion que crea un circulo
#------------------------------------------------------------------------------------------------------------------------
def create_round_button(master, command=None):
    #Crear una imagen de un signo de pregunta el cual al precionarse despliega la imagen de ayuda al usuario
    size = 30
    background_color = "#4AC0CD"
    question_mark_color = "white"
    
    image = Image.new("RGBA", (size, size), background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial", 18)
    text = "?"
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    draw.text(text_position, text, fill=question_mark_color, font=font)

    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, size, size), fill=255)

    image.putalpha(mask)

    photo = ImageTk.PhotoImage(image)    #transformar de Pillow a PhotoImage para usarse con Tkinter

    button = tk.Button(master, image=photo, relief="flat", bd=0, command=command)
    button.image = photo

    return button
#!------------------------------------------------------------------------------------------------------------------------!
#aqui comienza la creacion de la ventana
#!------------------------------------------------------------------------------------------------------------------------!
window = tk.Tk()
window.title("Cálculo de Aceleración")

input_frame = tk.Frame(window)
input_frame.pack(side="top", pady=10)

#!------------------------------------------------------------------------------------------------------------------------!
#cada grupo se encarga de la visualizacion de su respectivo parametro siendo que cada grupo comparte los comentarios 
#!------------------------------------------------------------------------------------------------------------------------!

#grupo encargado del angulo 
angulo_group = tk.Frame(input_frame)
angulo_label = tk.Label(angulo_group, text="Ángulo:")#crea enl titulo del recuadro
angulo_entry = tk.Entry(angulo_group)#campo de entrada 
#esta linea se encarga de la posision del boton de ayuda y su funcion
round_button1 = create_round_button(angulo_group, command=abrir_ventana_ayuda_angulo)
angulo_group.pack(side="top"), angulo_label.pack(side="top"), angulo_entry.pack(side="top"), round_button1.pack(side="top")


#Grupo de la masa 
masa_group = tk.Frame(input_frame)
masa_label = tk.Label(masa_group, text="Masa:")
masa_entry = tk.Entry(masa_group)
round_button2 = create_round_button(masa_group, command=abrir_ventana_ayuda_masa)
masa_group.pack(side="top"), masa_label.pack(side="top"), masa_entry.pack(side="top"), round_button2.pack(side="top")

#Grupo encargado de la visualizacion de la roce
coeficiente_roce_group = tk.Frame(input_frame)
coeficiente_roce_label = tk.Label(coeficiente_roce_group, text="Coeficiente de Roce:")
coeficiente_roce_entry = tk.Entry(coeficiente_roce_group)
round_button3 = create_round_button(coeficiente_roce_group, command=abrir_ventana_ayuda_coeficiente_roce)
coeficiente_roce_group.pack(side="top"), coeficiente_roce_label.pack(side="top"), coeficiente_roce_entry.pack(side="top"), round_button3.pack(side="top")

#Botón de cálculo
calcular_button = tk.Button(window, text="Calcular", command=calcular_button_click)
calcular_button.pack()

#Variable de texto para mostrar el resultado
resultado_text = tk.StringVar()
resultado_label = tk.Label(window, textvariable=resultado_text)
resultado_label.pack()

canvas = tk.Canvas(window, width=600, height=450)
canvas.pack()

dibujar_triangulo(45)#dibuja un triangulo base 

#Se utiliza un loop para crear el bucle principal de la interfaz gráfica.
window.mainloop() 