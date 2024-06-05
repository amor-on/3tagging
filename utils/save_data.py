import streamlit as st

def format_select(row, tag_name):
    block_title = row['block_title']
    block_key = f'block_{block_title}'
    return st.session_state['content_tags'].get(block_key, {}).get(tag_name, "")

def format_multiselect(row, tag_name):
    block_title = row['block_title']
    block_key = f'block_{block_title}'
    tags = st.session_state['content_tags'].get(block_key, {}).get(tag_name, {})
    return ", ".join(
        f"{k}:{v:.2f}" if isinstance(v, float) else f"{k}:NA"
        for k, v in tags.items()
    )

def format_float(row, tag_name):
    block_title = row['block_title']
    block_key = f'block_{block_title}'
    value = st.session_state['content_tags'].get(block_key, {}).get(tag_name, 0.0)
    return f"{value:.2f}"

def format_bool(row, tag_name):
    block_title = row['block_title']
    block_key = f'block_{block_title}'
    return st.session_state['content_tags'].get(block_key, {}).get(tag_name, False)

def apply_formatting(block_data, tags_schema, aggregation_levels):
    for tag in tags_schema:
        if any(level in aggregation_levels for level in tag['aggregation_level']):
            tag_name = tag['name']
            if tag['type'] == 'select':
                block_data[tag_name] = block_data.apply(lambda row: format_select(row, tag_name), axis=1)
            elif tag['type'] == 'multiselect':
                block_data[tag_name] = block_data.apply(lambda row: format_multiselect(row, tag_name), axis=1)
            elif tag['type'] == 'float':
                block_data[tag_name] = block_data.apply(lambda row: format_float(row, tag_name), axis=1)
            elif tag['type'] == 'bool':
                block_data[tag_name] = block_data.apply(lambda row: format_bool(row, tag_name), axis=1)
    return block_data

def save_tagged_data(contents, tags_schema, block_output_path, card_output_path):
    # Save block-level data (aggregation level 1)
    block_data = contents.copy()
    block_data = apply_formatting(block_data, tags_schema, aggregation_levels=[1])
    block_columns = ['stage', 'course', 'content', 'age', 'subject', 'unit_type', 'unit_title', 'card_title', 'block_title', 'card_type', 'block_type', 'text'] + [tag['name'] for tag in tags_schema if 1 in tag['aggregation_level']]
    block_data = block_data[block_columns]
    block_data.to_csv(block_output_path, index=False)

    # Save card-level data (aggregation level 2)
    card_data = contents.drop(columns=['block_title', 'block_type', 'text']).drop_duplicates()
    card_data['card_text'] = card_data['card_title'].apply(lambda card: "\n".join(contents[contents['card_title'] == card]['text'].tolist()))

    def format_card_select(card, tag_name):
        return st.session_state['content_tags'].get(f"card_{card}", {}).get(tag_name, "")

    def format_card_multiselect(card, tag_name):
        tags = st.session_state['content_tags'].get(f"card_{card}", {}).get(tag_name, {})
        return ", ".join(
            f"{k}:{v:.2f}" if isinstance(v, float) else f"{k}:NA"
            for k, v in tags.items()
        )

    def format_card_float(card, tag_name):
        value = st.session_state['content_tags'].get(f"card_{card}", {}).get(tag_name, 0.0)
        return f"{value:.2f}"

    def format_card_bool(card, tag_name):
        return st.session_state['content_tags'].get(f"card_{card}", {}).get(tag_name, False)

    for tag in tags_schema:
        if 2 in tag['aggregation_level']:
            tag_name = tag['name']
            if tag['type'] == 'select':
                card_data[tag_name] = card_data['card_title'].apply(lambda card: format_card_select(card, tag_name))
            elif tag['type'] == 'multiselect':
                card_data[tag_name] = card_data['card_title'].apply(lambda card: format_card_multiselect(card, tag_name))
            elif tag['type'] == 'float':
                card_data[tag_name] = card_data['card_title'].apply(lambda card: format_card_float(card, tag_name))
            elif tag['type'] == 'bool':
                card_data[tag_name] = card_data['card_title'].apply(lambda card: format_card_bool(card, tag_name))

    card_columns = ['stage', 'course', 'content', 'age', 'subject', 'unit_type', 'unit_title', 'card_title', 'card_type', 'card_text'] + [tag['name'] for tag in tags_schema if 2 in tag['aggregation_level']]
    card_data = card_data[card_columns]
    card_data.to_csv(card_output_path, index=False)
