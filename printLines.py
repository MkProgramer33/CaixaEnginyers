import numpy as np
import matplotlib.pyplot as plt

 

# Punto central
central_point = (2.8022296, 41.8954981)

# Lista de ángulos
angles = [-2.8091887247333607, -2.6537714727402157, 1.0186754794265944, 2.527020753707441]

#angles = [-0.7856969690407889,-0.8108131860731402,-0.792721874421991, -0.7812215553410897]
# Crear la figura y los ejes
fig, ax = plt.subplots()

# Dibujar el punto central
ax.plot(central_point[0], central_point[1], 'ro')  # Punto central en rojo

# Dibujar las líneas
for angle in angles:
    # Calcular las coordenadas de los extremos de la línea
    x_end = central_point[0] + np.cos(angle) * 10  # Escalar por 10 para hacer las líneas más largas
    y_end = central_point[1] + np.sin(angle) * 10
    ax.plot([central_point[0], x_end], [central_point[1], y_end], 'b-')  # Líneas en azul

# Ajustar la visualización
ax.set_aspect('equal')
ax.set_xlim(central_point[0] - 15, central_point[0] + 15)
ax.set_ylim(central_point[1] - 15, central_point[1] + 15)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Líneas desde el punto central')

# Mostrar la cuadrícula
ax.grid(True)

# Mostrar la figura
plt.show()
