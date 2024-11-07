import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definir funciones de frecuencia y magnitud para cada segmento
def f1(t):
    return 125 + 37000 * t

def M1(t):
    return 50 + 15000 * t

def f2(t):
    return 495 - 43250 * (t - 0.01)

def M2(t):
    return 200 - 17500 * (t - 0.01)

def f3(t):
    return 62.5 - 6250 * (t - 0.02)

def M3(t):
    return 25 - 2500 * (t - 0.02)

# Definir las transformadas de Fourier para cada segmento
def F1(f):
    real_part = lambda t: M1(t) * np.cos(2 * np.pi * (f1(t) - f) * t)
    imag_part = lambda t: M1(t) * np.sin(2 * np.pi * (f1(t) - f) * t)
    real_integral = quad(real_part, 0, 0.01)[0]
    imag_integral = quad(imag_part, 0, 0.01)[0]
    return real_integral + 1j * imag_integral

def F2(f):
    real_part = lambda t: M2(t) * np.cos(2 * np.pi * (f2(t) - f) * t)
    imag_part = lambda t: M2(t) * np.sin(2 * np.pi * (f2(t) - f) * t)
    real_integral = quad(real_part, 0.01, 0.02)[0]
    imag_integral = quad(imag_part, 0.01, 0.02)[0]
    return real_integral + 1j * imag_integral

def F3(f):
    real_part = lambda t: M3(t) * np.cos(2 * np.pi * (f3(t) - f) * t)
    imag_part = lambda t: M3(t) * np.sin(2 * np.pi * (f3(t) - f) * t)
    real_integral = quad(real_part, 0.02, 0.03)[0]
    imag_integral = quad(imag_part, 0.02, 0.03)[0]
    return real_integral + 1j * imag_integral

# Combinar las transformadas
def F_total(f):
    return F1(f) + F2(f) + F3(f)

# Función para actualizar la gráfica
def update_plot():
    f = float(f_entry.get())
    f_values = np.arange(0, 1001, 1)
    F_total_values = np.array([F_total(f_val) for f_val in f_values])
    
    ax.clear()
    ax.plot(f_values, np.abs(F_total_values))
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Magnitud')
    ax.set_title(f'Transformada de Fourier Total para f = {f}')
    ax.grid(True)
    canvas.draw()

# Crear la ventana principal
root = tk.Tk()
root.title("Transformada de Fourier Interactiva")

# Crear la figura de matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el canvas para la figura de matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Crear el cuadro de entrada para la frecuencia
f_label = tk.Label(root, text="Frecuencia f:")
f_label.pack()
f_entry = tk.Entry(root)
f_entry.pack()

# Crear el botón para actualizar la gráfica
update_button = tk.Button(root, text="Actualizar Gráfica", command=update_plot)
update_button.pack()

# Ejecutar la aplicación
root.mainloop()