import streamlit as st

def save_tagged_data(contents, tags_schema, block_output_path, card_output_path):
    # Save block-level data
    block_data = contents.copy()
    for tag in tags_schema:
        if tag['type'] == 'select':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state.get(f"{tag['name']}_select_block_{row['block_title']}", ""), axis=1)
        elif tag['type'] == 'multiselect':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state.get(f"{tag['name']}_multiselect_block_{row['block_title']}", []), axis=1)
        elif tag['type'] == 'float':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state.get(f"{tag['name']}_float_block_{row['block_title']}", 0.0), axis=1)
        elif tag['type'] == 'bool':
            block_data[tag['name']] = block_data.apply(lambda row: st.session_state.get(f"{tag['name']}_bool_block_{row['block_title']}", False), axis=1)
    block_data.to_csv(block_output_path, index=False)

    # Save card-level data
    card_data = contents.drop(columns=['block_title', 'block_type', 'text']).drop_duplicates()
    card_data['card_text'] = card_data['card_title'].apply(lambda card: "\n".join(contents[contents['card_title'] == card]['text'].tolist()))
    for tag in tags_schema:
        if tag['type'] == 'select':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state.get(f"{tag['name']}_select_card", ""))
        elif tag['type'] == 'multiselect':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state.get(f"{tag['name']}_multiselect_card", []))
        elif tag['type'] == 'float':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state.get(f"{tag['name']}_float_card", 0.0))
        elif tag['type'] == 'bool':
            card_data[tag['name']] = card_data['card_title'].apply(lambda card: st.session_state.get(f"{tag['name']}_bool_card", False))
    card_data.to_csv(card_output_path, index=False)
