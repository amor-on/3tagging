import streamlit as st
from streamlit_modal import Modal
from utils.data_loader import load_contents, load_tags_schema
from components.sidebar import render_sidebar
from components.tag_form import render_tag_form
from utils.save_data import save_tagged_data
from utils.navigation import Navigation

# Inicializar el estado de la sesión
if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0
if 'current_block_index' not in st.session_state:
    st.session_state.current_block_index = 0
if 'view' not in st.session_state:
    st.session_state.view = 'card'

# Cargar los datos
contents = load_contents('data/contents.csv')
tags_schema = load_tags_schema('data/tags_schema.json')

# Inicializar la navegación
if 'nav' not in st.session_state:
    st.session_state.nav = Navigation(contents)

nav = st.session_state.nav

st.set_page_config(layout="wide")
st.title('Aplicación de Etiquetado de Contenidos Educativos')

# Importar CSS
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Renderizar la barra lateral
selected_card = render_sidebar(nav)
current_card_title = nav.get_current_card()
card_data = contents[contents['card_title'] == current_card_title]

# Crear columnas para contenido y formulario de etiquetado
col1, col2 = st.columns([1, 1])

with col1:
    st.header(f'Contenido de la Tarjeta: {current_card_title}')
    if not card_data.empty:
        for block_index, (i, row) in enumerate(card_data.iterrows()):
            with st.container():
                st.subheader(row['block_title'])
                st.markdown(f"**{row['subject']}** > **{row['card_title']}** ({row['card_type']}) > **{row['block_title']}** ({row['block_type']})")
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
                
                # Botón para abrir el modal de etiquetado del bloque
                modal = Modal(f"Etiquetar Bloque *{row['block_title']}*", key=f"modal-{block_index}")
                if st.button(f"Etiquetar Bloque *{row['block_title']}*", key=f"button-{block_index}"):
                    modal.open()
#  st.header(f"Etiquetas del Bloque: {block_data['block_title']}")
 
                if modal.is_open():
                    with modal.container():
                        render_tag_form(tags_schema, current_card_title, contents, block_index)
                        if st.button("Guardar Etiquetas", key=f"save-{block_index}"):
                            st.session_state.saved = True
                            st.experimental_rerun()
    else:
        st.write("No se encontró contenido para la tarjeta seleccionada.")

with col2:
    # Mostrar un encabezado para el formulario de etiquetado general
    st.header('Formulario de Etiquetado General')
    render_tag_form(tags_schema, current_card_title, contents)

# Botón para guardar progreso
if st.button('Guardar Progreso'):
    block_output_path = 'data/contents_tagged.csv'
    card_output_path = 'data/cards_tagged.csv'
    save_tagged_data(contents, tags_schema, block_output_path, card_output_path)
    st.success('Progreso guardado correctamente.')
