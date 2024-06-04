import streamlit as st

def render_sidebar(nav, contents):
    st.sidebar.title('Selector de Tarjetas')

    # Obtener las unidades únicas del DataFrame
    units = contents['unit_title'].unique()

    # Verificar si se ha seleccionado una nueva unidad
    if 'current_unit' not in st.session_state:
        st.session_state.current_unit = units[0]  # Seleccionar la primera unidad por defecto
    selected_unit = st.sidebar.selectbox('Seleccionar Unidad', units, index=list(units).index(st.session_state.current_unit))
    
    # Filtrar el DataFrame para obtener las tarjetas de la unidad seleccionada
    unit_contents = contents[contents['unit_title'] == selected_unit]
    card_titles = unit_contents['card_title'].unique().tolist()

    # Verificar si se ha seleccionado una nueva unidad
    if selected_unit != st.session_state.current_unit:
        st.session_state.current_unit = selected_unit
        st.session_state.current_card_index = 0
        st.session_state.current_card_title = card_titles[0] if card_titles else ""  # Reiniciar al seleccionar una nueva unidad
        nav.current_card_index = st.session_state.current_card_index
        st.experimental_rerun()

    # Verificar si se ha seleccionado una nueva tarjeta
    if 'current_card_title' not in st.session_state or st.session_state.current_card_title not in card_titles:
        st.session_state.current_card_title = card_titles[0] if card_titles else ""  # Seleccionar la primera tarjeta por defecto
    selected_card = st.sidebar.selectbox('Seleccionar Tarjeta', card_titles, index=card_titles.index(st.session_state.current_card_title))

    # Actualizar el estado si se selecciona una nueva tarjeta
    if selected_card != st.session_state.current_card_title:
        st.session_state.current_card_title = selected_card
        st.session_state.current_card_index = card_titles.index(selected_card)
        st.session_state.current_block_index = 0
        nav.current_card_index = st.session_state.current_card_index
        nav.current_block_index = st.session_state.current_block_index
        st.experimental_rerun()

    # Botones de navegación
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button('Anterior'):
            if st.session_state.current_card_index > 0:
                st.session_state.current_card_index -= 1
                st.session_state.current_card_title = card_titles[st.session_state.current_card_index]
                st.session_state.current_block_index = 0
                nav.current_card_index = st.session_state.current_card_index
                nav.current_block_index = st.session_state.current_block_index
                st.experimental_rerun()
    with col2:
        if st.button('Siguiente'):
            if st.session_state.current_card_index < len(card_titles) - 1:
                st.session_state.current_card_index += 1
                st.session_state.current_card_title = card_titles[st.session_state.current_card_index]
                st.session_state.current_block_index = 0
                nav.current_card_index = st.session_state.current_card_index
                nav.current_block_index = st.session_state.current_block_index
                st.experimental_rerun()

    return selected_card
