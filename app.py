import streamlit as st
from utils.data_loader import load_contents, load_tags_schema
from components.sidebar import render_sidebar
from components.tag_form import render_tag_form
from utils.save_data import save_tagged_data
from utils.navigation import Navigation
import pandas as pd
from streamlit_extras.stylable_container import stylable_container

# Inicializar el estado de la sesión
if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0
if 'current_block_index' not in st.session_state:
    st.session_state.current_block_index = 0
if 'view' not in st.session_state:
    st.session_state.view = 'card'
if 'content_tags' not in st.session_state:
    st.session_state.content_tags = {}

# Cargar los datos
contents = load_contents('data/contents.csv')
tags_schema = load_tags_schema('data/tags_schema.json')

# Asegurarse de que contents es un DataFrame
if not isinstance(contents, pd.DataFrame):
    raise TypeError("contents debe ser un DataFrame")

# Inicializar la navegación
if 'nav' not in st.session_state:
    st.session_state.nav = Navigation(contents)

nav = st.session_state.nav

st.set_page_config(
    page_title="Etiquetado",
    layout="wide",
    page_icon=":large_red_square:"
)

st.title('Etiquetado de contenidos')

# Importar CSS
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Renderizar la barra lateral
selected_card = render_sidebar(nav, contents)
current_card_title = st.session_state.current_card_title
card_data = contents[contents['card_title'] == current_card_title]

# Crear columnas para contenido y formulario de etiquetado
col1, col2 = st.columns([1, 1])

# Hacer la columna 1 fija
with col1:
    st.markdown('<div class="fixed-column">', unsafe_allow_html=True)
    st.header(f'Tarjeta: *{current_card_title}*')
    if not card_data.empty:
        for block_index, (i, row) in enumerate(card_data.iterrows()):
            with st.container():
                st.subheader(row['block_title'])

                with stylable_container(
                    key="green_popover",
                    css_styles="""
                    button {
                        height: 20px;
                        background-color: #5497AD;
                        color: white;
                        border-radius: 10px;
                        white-space: nowrap;
                    }""",
                ):
                    with st.popover(label=f"Etiquetar ***{row['block_title']}***"): 
                        render_tag_form(tags_schema, current_card_title, contents, block_index)
                
                text_content = row['text']
                text_lines = text_content.split('\n')
                for line in text_lines:
                    if line.startswith("http"):
                        if any(ext in line for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                            st.image(line)
                        elif any(ext in line for ext in ['.mp4', '.webm']):
                            st.video(line)
                        elif any(ext in line for ext in ['.mp3', '.wav', '.ogg']):
                            st.audio(line)
                        else:
                            st.write(line)
                    else:
                        st.write(line)
    else:
        st.write("No se encontró contenido para la tarjeta seleccionada.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Crear un contenedor con scroll para el formulario de etiquetado
    st.header('Etiquetado de la tarjeta')
    with st.popover("Etiquetar Tarjeta"):
        render_tag_form(tags_schema, current_card_title, contents)

# Botón para guardar progreso
if st.button('Guardar Progreso', key='save_progress'):
    card_output_path = 'data/cards_tagged.csv'
    save_tagged_data(contents, tags_schema, None, card_output_path)
    st.success('Progreso guardado correctamente.')
    
    # Cargar los datos guardados
    tagged_card = pd.read_csv(card_output_path)
    
    # Crear el botón de descarga
    st.download_button(
        label="Descargar CSV de tarjeta etiquetada",
        data=tagged_card.to_csv(index=False).encode('utf-8'),
        file_name='card_tagged.csv',
        mime='text/csv'
    )
