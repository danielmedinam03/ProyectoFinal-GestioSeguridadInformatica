import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap, BoundaryNorm


# Función genérica para generar el mapa de calor
def generar_mapa(datos, titulo, col_title):
    # Información de valoraciones de amenazas
    valoraciones = {
        1: 'Muy frecuente (MF)',
        2: 'Frecuente (F)',
        3: 'Normal (N)',
        4: 'Poco frecuente (PF)',
        5: 'Muy poco frecuente (MPF)'
    }

    # Rango de impactos
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 9)]

    # Crear una matriz de ceros
    matriz_calor = np.zeros((len(valoraciones), len(rangos)))

    # Llenar la matriz con los datos
    for _, valoracion_id, impacto_potencial, impacto_residual in datos:
        if col_title == 'Impacto Potencial':
            impacto = impacto_potencial
        else:
            impacto = impacto_residual

        if valoracion_id in valoraciones:
            for j, (min_rango, max_rango) in enumerate(rangos):
                if min_rango < impacto <= max_rango:
                    matriz_calor[valoracion_id - 1, j] += 1

    # Crear etiquetas para los ejes
    etiquetas_y = [valoraciones[i] for i in range(1, len(valoraciones) + 1)]
    etiquetas_x = [f'({min_rango}-{max_rango})' for min_rango, max_rango in rangos]

    # Crear DataFrame para el mapa de calor
    df_calor = pd.DataFrame(matriz_calor, index=etiquetas_y, columns=etiquetas_x)

    # Definir los colores personalizados
    colors = ['#00ff00', '#ffff00', '#ffcc00', '#ff9900', '#ff0000']  # Verde, amarillo, rojo
    cmap = ListedColormap(colors)
    bounds = [0, 1, 2, 3, 4, 5]
    norm = BoundaryNorm(bounds, cmap.N)

    # Crear el mapa de calor con seaborn
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df_calor, annot=True, cmap=cmap, linewidths=.5, linecolor='black', ax=ax, norm=norm, cbar_kws={'boundaries': bounds, 'ticks': [1, 2, 3, 4, 5]})
    ax.set_title('Mapa de Calor de Valoración de Amenazas')
    ax.set_xlabel(col_title)
    ax.set_ylabel('Valoración de Amenazas')

    # Mostrar el mapa de calor en Streamlit
    st.title(titulo)
    st.pyplot(fig)


# def generar_mapa_antes(datos):

#     print(datos)

#     data = datos

#     # Información de valoraciones de amenazas
#     valoraciones = {
#         1: 'Muy frecuente (MF)',
#         2: 'Frecuente (F)',
#         3: 'Normal (N)',
#         4: 'Poco frecuente (PF)',
#         5: 'Muy poco frecuente (MPF)'
#     }

#     # Rango de impactos
#     rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 9)]

#     # Crear una matriz de ceros
#     matriz_calor = np.zeros((len(valoraciones), len(rangos)))

#     # Llenar la matriz con los datos
#     for _, valoracion_id, impacto, _ in data:
        
#         if valoracion_id in valoraciones:
#             print("Valoracion id:" + str(valoracion_id))
#             for j, (min_rango, max_rango) in enumerate(rangos):

#                 if min_rango < impacto <= max_rango:

#                     matriz_calor[valoracion_id - 1, j] += 1

#     print(matriz_calor)

#     # Crear etiquetas para los ejes
#     etiquetas_y = [valoraciones[i] for i in range(1, len(valoraciones) + 1)]
#     etiquetas_x = [f'({min_rango}-{max_rango})' for min_rango, max_rango in rangos]

#     # Crear DataFrame para el mapa de calor
#     df_calor = pd.DataFrame(matriz_calor, index=etiquetas_y, columns=etiquetas_x)

#     # Definir los colores personalizados
#     colors = ['#00ff00', '#ffff00', '#ffcc00', '#ff9900', '#ff0000']  # Verde, amarillo, rojo
#     cmap = ListedColormap(colors)
#     bounds = [0, 1, 2, 3, 4, 5]
#     norm = BoundaryNorm(bounds, cmap.N)
#     # Crear el mapa de calor con seaborn
#     fig, ax = plt.subplots(figsize=(10, 8))
#     sns.heatmap(df_calor, annot=True, cmap=cmap, linewidths=.5, linecolor='black', ax=ax, norm=norm, cbar_kws={'boundaries': bounds, 'ticks': [1, 2, 3, 4, 5]})
#     ax.set_title('Mapa de Calor de Valoración de Amenazas')
#     ax.set_xlabel('Impacto Potencial')
#     ax.set_ylabel('Valoración de Amenazas')

#     # Mostrar el mapa de calor en Streamlit
#     st.title('Mapa de Calor antes de los salvaguardas')
#     st.pyplot(fig)

# def generar_mapa_despues(datos):
#     print(datos)

#     data = datos

#     # Información de valoraciones de amenazas
#     valoraciones = {
#         1: 'Muy frecuente (MF)',
#         2: 'Frecuente (F)',
#         3: 'Normal (N)',
#         4: 'Poco frecuente (PF)',
#         5: 'Muy poco frecuente (MPF)'
#     }

#     # Rango de impactos
#     rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 9)]

#     # Crear una matriz de ceros
#     matriz_calor = np.zeros((len(valoraciones), len(rangos)))

#     # Llenar la matriz con los datos
#     for _, valoracion_id, _, impacto in data:
        
#         if valoracion_id in valoraciones:
#             print("Valoracion id:" + str(valoracion_id))
#             for j, (min_rango, max_rango) in enumerate(rangos):

#                 if min_rango < impacto <= max_rango:

#                     matriz_calor[valoracion_id - 1, j] += 1

#     print(matriz_calor)

#     # Crear etiquetas para los ejes
#     etiquetas_y = [valoraciones[i] for i in range(1, len(valoraciones) + 1)]
#     etiquetas_x = [f'({min_rango}-{max_rango})' for min_rango, max_rango in rangos]

#     # Crear DataFrame para el mapa de calor
#     df_calor = pd.DataFrame(matriz_calor, index=etiquetas_y, columns=etiquetas_x)

#     # Definir los colores personalizados
#     colors = ['#00ff00', '#ffff00', '#ffcc00', '#ff9900', '#ff0000']  # Verde, amarillo, rojo
#     cmap = ListedColormap(colors)
#     bounds = [0, 1, 2, 3, 4, 5]
#     norm = BoundaryNorm(bounds, cmap.N)
#     # Crear el mapa de calor con seaborn
#     fig, ax = plt.subplots(figsize=(10, 8))
#     sns.heatmap(df_calor, annot=True, cmap=cmap, linewidths=.5, linecolor='black', ax=ax, norm=norm, cbar_kws={'boundaries': bounds, 'ticks': [1, 2, 3, 4, 5]})
#     ax.set_title('Mapa de Calor de Valoración de Amenazas')
#     ax.set_xlabel('Impacto Potencial')
#     ax.set_ylabel('Valoración de Amenazas')

#     # Mostrar el mapa de calor en Streamlit
#     st.title('Mapa de Calor después de los salvaguardas')
#     st.pyplot(fig)
