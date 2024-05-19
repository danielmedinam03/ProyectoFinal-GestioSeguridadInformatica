# Importación de librerías necesarias
import streamlit as st
from streamlit_option_menu import option_menu

from consultas_bd import *
from insert_data import *
from config import connect_to_database
from grafico import *

# Inicializar el estado de la sesión si es necesario
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = []
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []

# Definición de la función principal del streamlit app
def main():

    with st.sidebar:
        selected = option_menu("Menu", ["Formulario", 'Mapas de calor'],
                               icons=['house', 'gear'], menu_icon="cast", default_index=0)
    # Conexión a la base de datos
    connection = connect_to_database("localhost", "root", "Dfmm.03112002", "gestion_seguridad")

    if selected == "Formulario":
        
    # Título del dashboard
        st.title("Registro de activos")
        dictionario_final = {}
        
        # Nombre de activo
        nombre_activo = st.text_input(label="Ingresa el nombre del activo:")

        # Tipos de activos
        result_tipos_activos = consulta_tipos_activos(connection)
        tipo_activo = st.selectbox('Elige el tipo de activo:', list(result_tipos_activos.keys()), placeholder='Seleccione un tipo de activo...')
        tipo_activo_selected_id = result_tipos_activos[tipo_activo] if tipo_activo in result_tipos_activos else None

        # Tipos de amenazas        
        result_tipos_amenazas = consulta_tipo_amenaza(connection)
        tipos_amenazas = st.multiselect('Elige los tipos de amenazas:', list(result_tipos_amenazas.keys()),
                                        key='selected_category', placeholder="Seleccione una amenaza...")
        
        # Amenazas
        result_amenazas = consulta_amenaza(connection,tipos_amenazas)
        amenazas = st.multiselect("Selecciona las amenazas:", result_amenazas, key='selected_items', 
                                        placeholder="Seleccione los tipos de amenazas...")

        #Se obtiene el valor de la escala de valor
        escala_valor = consulta_escalar_valor(connection)
        
        #Declaracion de variables
        dict_amenazas = {}
        probabilidad = 0
        riesgo_potencial = 0

        if amenazas != []:
            for index, item in enumerate(amenazas):
                suma_impacto_potencial = 0

                st.subheader(f"Valor de: {item}")
                valor_col1, valor_col2, valor_col3 = st.columns(3)
                list_detalle_valor = {}
                with valor_col1:
                    #Se selecciona el nombre de la escala valor
                    valor_confidencialidad = st.selectbox("Confidencialidad:", list(escala_valor.keys()), key=f'valor_confidencialidad_{index}')
                    #Se extrae el id de la escala valor seleccionada
                    valor_confidencialidad_selected_id = escala_valor[valor_confidencialidad] if valor_confidencialidad in escala_valor else None
                    #Se otiene el valor numerico para el impacto potencial
                    valor_confidencialidad_selected = consulta_valor_escala_valor(connection,valor_confidencialidad_selected_id)
                    suma_impacto_potencial += valor_confidencialidad_selected
                    list_detalle_valor[3] = valor_confidencialidad_selected_id

                with valor_col2:
                    valor_integridad = st.selectbox("Integridad:", list(escala_valor.keys()), key=f'valor_integridad_{index}')
                    valor_integridad_selected_id = escala_valor[valor_integridad] if valor_integridad in escala_valor else None
                    valor_integridad_selected = consulta_valor_escala_valor(connection,valor_integridad_selected_id)
                    suma_impacto_potencial += valor_integridad_selected
                    list_detalle_valor[2] = valor_integridad_selected_id

                with valor_col3:
                    valor_disponibilidad = st.selectbox("Disponibilidad:", list(escala_valor.keys()), key=f'valor_disponibilidad_{index}')
                    valor_disponibilidad_selected_id = escala_valor[valor_disponibilidad] if valor_disponibilidad in escala_valor else None
                    valor_disponibilidad_selected = consulta_valor_escala_valor(connection,valor_disponibilidad_selected_id)
                    suma_impacto_potencial += valor_disponibilidad_selected
                    list_detalle_valor[1] = valor_disponibilidad_selected_id
                
                # Impacto potencial
                st.markdown("<div style='text-align: right'><b>Impacto potencial: " + str(suma_impacto_potencial) + "</b></div>", unsafe_allow_html=True)
                
                # Probabilidad
                probabilidad = st.selectbox("Probabilidad: ", list(opciones_probabilidad(consulta_probabilidad(connection))), key=f'probabilidad_{index}')
                valor_probabilidad = consulta_valor_probabilidad(connection,probabilidad)
                valoracion_amenaza_id = consulta_id_probabilidad(connection,probabilidad)

                # Riesgo potencial
                riesgo_potencial = valor_probabilidad * suma_impacto_potencial
                st.markdown("<div style='text-align: right'><b>Riesgo potencial: " + str(riesgo_potencial) + "</b></div>", unsafe_allow_html=True   )       
                
                # Tipo Salvaguardas
                st.markdown("### Salvaguardas")
                tipo_salvaguarda_dict = consulta_tipo_salvaguarda(connection)
                tipo_salvaguarda_selected = st.selectbox("Tipo de salvaguarda: ", list(tipo_salvaguarda_dict.keys()), key=f'tipo_salvaguarda_{index}')
                tipo_salvaguarda_selected_id = tipo_salvaguarda_dict[tipo_salvaguarda_selected]

                # Salvaguarda
                salvaguarda_dict = consulta_salvaguarda(connection, tipo_salvaguarda_selected_id)
                salvaguarda_selected = st.selectbox("Tipo de salvaguarda: ", list(salvaguarda_dict.keys()), key=f'salvaguarda_{index}')
                salvaguarda_selected_id = salvaguarda_dict[salvaguarda_selected]

                # Valoracion de salvaguarda
                valoracion_salvaguarda_dict = consulta_valoracion_salvaguarda(connection)
                valoracion_salvaguarda_selected = st.selectbox("Valoración de salvaguarda: ", list(valoracion_salvaguarda_dict.keys()), key=f'valoracion_salvaguarda_{index}')
                valoracion_salvaguarda_selected_id = valoracion_salvaguarda_dict[valoracion_salvaguarda_selected]

                # Impacto residual  
                factor = consulta_factor_valoracion_salvaguarda(connection,valoracion_salvaguarda_selected_id)
                impacto_residual = round(suma_impacto_potencial - (suma_impacto_potencial * factor),1)

                st.markdown("<div style='text-align: right'><b>Impacto residual: " + str(impacto_residual) + "</b></div>", unsafe_allow_html=True)

                # Riesgo residual
                riesgo_residual = round(valor_probabilidad * impacto_residual,1)
                st.markdown("<div style='text-align: right'><b>Riesgo residual: " + str(riesgo_residual) + "</b></div>", unsafe_allow_html=True   )       

                st.markdown("---")

                #La idea es que aqui se de esta manera se guardan los valores, para luego crear una funcion que inserte los datos en la bd y reciba por parametro el diccionario
                amenaza_id = consulta_id_amenaza(connection,item)

                dict_amenazas[item] = {'amenaza_id':amenaza_id,'valores_ids': list_detalle_valor, 'impacto_potencial': suma_impacto_potencial, 
                                            'probabilidad': probabilidad, 'probabilidad_id': valoracion_amenaza_id,'valor_probabilidad': float(valor_probabilidad), 
                                            'riesgo_potencial': float(riesgo_potencial), 'tipo_salvaguarda': tipo_salvaguarda_selected_id,
                                            'salvaguarda': salvaguarda_selected_id, 'valoracion_salvaguarda': valoracion_salvaguarda_selected_id,
                                            'impacto_residual': float(impacto_residual), 'riesgo_residual': float(riesgo_residual)}

        # Botón para enviar el formulario completo
        submit_button = st.button("Enviar")

        #Llenado del diccionario
        dictionario_final['nombre_activo'] = nombre_activo
        dictionario_final['tipo_activo'] = tipo_activo_selected_id
        dictionario_final['amenazas'] = amenazas
        dictionario_final['dict_amenazas'] = dict_amenazas

        if (submit_button and len(amenazas) > 0 and (tipo_activo != 'Seleccione un tipo de activo...' and tipo_activo != '') 
            and len(tipos_amenazas) > 0 and nombre_activo != ''):
            
            print("Envio el Formulario")
            
            print(dictionario_final)
            print("-----------------------------------------------------------------------")

            construccion_query_insert_transaccion(conexion=connection, diccionario=dictionario_final)
            st.success("Se ha guardado correctamente !")
        else:
            # Mostrar mensaje de error
            st.warning("Completa el formulario correctamente antes de enviarlo.")
        
    elif selected == "Mapas de calor":        
        
        # Generar el mapa de calor antes de los salvaguardas
        generar_mapa(consulta_resumen_activo_amenaza(connection), 'Mapa de Calor antes de los salvaguardas', 'Impacto Potencial')

        # Generar el mapa de calor después de los salvaguardas
        generar_mapa(consulta_resumen_activo_amenaza(connection), 'Mapa de Calor después de los salvaguardas', 'Impacto Residual')


# Comentar esta línea antes de enviar el código al usuario
if __name__ == "__main__":
    main()
