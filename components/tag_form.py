import streamlit as st
from utils.tag_helpers import get_tags_for_level

def render_tag_form(tags_schema, selected_card_title, contents, block_index=None):
    card_data = contents[contents['card_title'] == selected_card_title]
    
    if block_index is not None:
        # Vista de bloque
        if not card_data.empty:
            block_data = card_data.iloc[block_index]
            tags_for_block = get_tags_for_level(tags_schema, 1)
            
            for tag in tags_for_block:
                tag_key = f"{tag['name']}_{tag['type']}_block_{block_data['block_title']}"
                if tag['type'] == 'select':
                    st.selectbox(f"**{tag['name']}**", tag['values'], help=tag['description'], key=tag_key)
                elif tag['type'] == 'multiselect':
                    selected_options = st.multiselect(f"**{tag['name']}**", tag['values'], help=tag['description'], key=tag_key)
                    for option in selected_options:
                        if tag['quantifiable']:
                            slider_key = f"{tag['name']}_{option}_slider_block_{block_data['block_title']}"
                            st.slider(f"Relevancia para {option}", 0.0, 1.0, 1.0, step=0.01, format="%.2f", key=slider_key)
                elif tag['type'] == 'float':
                    st.slider(f"**{tag['name']}**", 0.0, 1.0, help=tag['description'], key=tag_key)
                elif tag['type'] == 'bool':
                    st.radio(f"**{tag['name']}**", [True, False], help=tag['description'], key=tag_key)
        else:
            st.write("No se encontraron datos para el bloque seleccionado.")
    else:
        st.header('Formulario de Etiquetado de la Tarjeta')
        # Vista de tarjeta completa
        if not card_data.empty:
            tags_for_card = get_tags_for_level(tags_schema, 2)
            st.subheader('Etiquetas de la Tarjeta')
            for tag in tags_for_card:
                tag_key = f"{tag['name']}_{tag['type']}_card"
                if tag['type'] == 'select':
                    st.selectbox(tag['name'], tag['values'], help=tag['description'], key=tag_key)
                elif tag['type'] == 'multiselect':
                    selected_options = st.multiselect(tag['name'], tag['values'], help=tag['description'], key=tag_key)
                    for option in selected_options:
                        if tag['quantifiable']:
                            slider_key = f"{tag['name']}_{option}_slider_card"
                            st.slider(f"Relevancia para {option}", 0.0, 1.0, 1.0, step=0.01, format="%.2f", key=slider_key)
                elif tag['type'] == 'float':
                    st.slider(tag['name'], 0.0, 1.0, help=tag['description'], key=tag_key)
                elif tag['type'] == 'bool':
                    st.radio(tag['name'], [True, False], help=tag['description'], key=tag_key)
        else:
            st.write("No se encontraron datos para la tarjeta seleccionada.")
