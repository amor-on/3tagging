import streamlit as st

def save_tagged_data(contents, tags_schema, block_output_path, card_output_path):
    # Save block-level data
    block_data = contents.copy()
    for tag in tags_schema:
        if tag['type'] == 'select':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state['content_tags'].get(f"block_{row['block_title']}", {}).get(tag['name'], ""), axis=1)
        elif tag['type'] == 'multiselect':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state['content_tags'].get(f"block_{row['block_title']}", {}).get(tag['name'], []), axis=1)
        elif tag['type'] == 'float':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state['content_tags'].get(f"block_{row['block_title']}", {}).get(tag['name'], 0.0), axis=1)
        elif tag['type'] == 'bool':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state['content_tags'].get(f"block_{row['block_title']}", {}).get(tag['name'], False), axis=1)
    block_data.to_csv(block_output_path, index=False)

    # Save card-level data
    card_data = contents.drop(columns=['block_title', 'block_type', 'text']).drop_duplicates()
    card_data['card_text'] = card_data['card_title'].apply(lambda card: "\n".join(contents[contents['card_title'] == card]['text'].tolist()))
    for tag in tags_schema:
        if tag['type'] == 'select':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state['content_tags'].get(f"card_{card}", {}).get(tag['name'], ""))
        elif tag['type'] == 'multiselect':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state['content_tags'].get(f"card_{card}", {}).get(tag['name'], []))
        elif tag['type'] == 'float':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state['content_tags'].get(f"card_{card}", {}).get(tag['name'], 0.0))
        elif tag['type'] == 'bool':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state['content_tags'].get(f"card_{card}", {}).get(tag['name'], False))
    card_data.to_csv(card_output_path, index=False)
