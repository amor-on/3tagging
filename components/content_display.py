import streamlit as st

def display_card_content(contents, selected_card_title):
    st.header(f'ETIQUETANDO TARJETA {selected_card_title}')
    card_data = contents[contents['card_title'] == selected_card_title]
    
    if not card_data.empty:
        for _, row in card_data.iterrows():
            st.subheader(row['block_title'])
            
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

def display_block_content(contents, selected_card_title, block_index):
    st.header(f'ETIQUETANDO BLOQUE {block_index + 1} DE LA TARJETA {selected_card_title}')
    card_data = contents[contents['card_title'] == selected_card_title]
    
    if not card_data.empty:
        if block_index < len(card_data):
            block_data = card_data.iloc[block_index]
            st.subheader(block_data['block_title'])
            
            text_content = block_data['text']
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
            st.write("El índice del bloque está fuera de los límites.")
    else:
        st.write("No se encontró contenido para el bloque seleccionado.")