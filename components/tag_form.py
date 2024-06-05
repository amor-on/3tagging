import streamlit as st
from utils.tag_helpers import get_tags_for_level

def render_tag_form(tags_schema, selected_card_title, contents, block_index=None):
    card_data = contents[contents['card_title'] == selected_card_title]
    
    if block_index is not None:
        # Vista de bloque
        if not card_data.empty:
            block_data = card_data.iloc[block_index]
            tags_for_block = get_tags_for_level(tags_schema, 1)
            
            block_tags = {}
            for tag in tags_for_block:
                tag_key = f"{tag['name']}_{tag['type']}_block_{block_data['block_title']}_{block_index}"
                current_value = st.session_state['content_tags'].get(f"block_{block_data['block_title']}", {}).get(tag['name'], None)
                
                if tag['type'] == 'select':
                    block_tags[tag['name']] = st.selectbox(
                        f"**{tag['name']}**", tag['values'], 
                        help=tag['description'], 
                        key=tag_key, 
                        index=tag['values'].index(current_value) if current_value else 0
                    )
                elif tag['type'] == 'multiselect':
                    selected_options = st.multiselect(
                        f"**{tag['name']}**", tag['values'], 
                        help=tag['description'], 
                        key=tag_key, 
                        default=list(current_value.keys()) if current_value else []
                    )
                    block_tags[tag['name']] = {
                        option: st.slider(
                            f"Relevancia para {option}", 0.0, 1.0, 
                            current_value[option] if current_value and option in current_value else 1.0,
                            step=0.01, format="%.2f", 
                            key=f"{tag_key}_{option}_slider"
                        ) if tag['quantifiable'] else "NA" for option in selected_options
                    }
                elif tag['type'] == 'float':
                    block_tags[tag['name']] = st.slider(
                        f"**{tag['name']}**", 0.0, 1.0, 
                        current_value if current_value is not None else 0.0, 
                        step=0.01, help=tag['description'], key=tag_key
                    )
                elif tag['type'] == 'bool':
                    block_tags[tag['name']] = st.radio(
                        f"**{tag['name']}**", [True, False], 
                        index=[True, False].index(current_value) if current_value is not None else 0, 
                        help=tag['description'], key=tag_key
                    )
            
            if st.button("Guardar Etiquetas", key=f"save_button_{selected_card_title}_{block_index}"):
                st.session_state['content_tags'][f"block_{block_data['block_title']}"] = block_tags
                st.rerun()
    else:
        # Vista de tarjeta completa
        if not card_data.empty:
            tags_for_card = get_tags_for_level(tags_schema, 2)
            
            card_tags = {}
            for tag in tags_for_card:
                tag_key = f"{tag['name']}_{tag['type']}_card_{selected_card_title}"
                current_value = st.session_state['content_tags'].get(f"card_{selected_card_title}", {}).get(tag['name'], None)
                
                if tag['type'] == 'select':
                    card_tags[tag['name']] = st.selectbox(
                        tag['name'], tag['values'], 
                        help=tag['description'], 
                        key=tag_key, 
                        index=tag['values'].index(current_value) if current_value else 0
                    )
                elif tag['type'] == 'multiselect':
                    selected_options = st.multiselect(
                        tag['name'], tag['values'], 
                        help=tag['description'], 
                        key=tag_key, 
                        default=list(current_value.keys()) if current_value else []
                    )
                    card_tags[tag['name']] = {
                        option: st.slider(
                            f"Relevancia para {option}", 0.0, 1.0, 
                            current_value[option] if current_value and option in current_value else 1.0,
                            step=0.01, format="%.2f", 
                            key=f"{tag_key}_{option}_slider"
                        ) if tag['quantifiable'] else "NA" for option in selected_options
                    }
                elif tag['type'] == 'float':
                    card_tags[tag['name']] = st.slider(
                        tag['name'], 0.0, 1.0, 
                        current_value if current_value is not None else 0.0, 
                        step=0.01, help=tag['description'], key=tag_key
                    )
                elif tag['type'] == 'bool':
                    card_tags[tag['name']] = st.radio(
                        tag['name'], [True, False], 
                        index=[True, False].index(current_value) if current_value is not None else 0, 
                        help=tag['description'], key=tag_key
                    )
            
            if st.button("Guardar Etiquetas", key=f"save_button_{selected_card_title}_card"):
                st.session_state['content_tags'][f"card_{selected_card_title}"] = card_tags
                st.rerun()
