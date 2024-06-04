import streamlit as st

def render_sidebar(nav):
    st.sidebar.title('Selector de Tarjetas')
    card_titles = nav.get_card_titles()

    # Utilizar un selectbox para la navegación de las tarjetas
    selected_card = st.sidebar.selectbox('Seleccionar Tarjeta', card_titles, index=st.session_state.current_card_index)
    
    if selected_card != nav.get_current_card():
        st.session_state.current_card_index = card_titles.index(selected_card)
        st.session_state.current_block_index = 0
        st.session_state.view = 'card'
        nav.current_card_index = st.session_state.current_card_index
        nav.current_block_index = st.session_state.current_block_index
        nav.view = st.session_state.view

    # Botones de navegación
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button('Anterior'):
            if st.session_state.current_card_index > 0:
                st.session_state.current_card_index -= 1
                st.session_state.current_block_index = 0
                st.session_state.view = 'card'
                nav.current_card_index = st.session_state.current_card_index
                nav.current_block_index = st.session_state.current_block_index
                nav.view = st.session_state.view
                st.rerun()
    with col2:
        if st.button('Siguiente'):
            if st.session_state.current_card_index < len(card_titles) - 1:
                st.session_state.current_card_index += 1
                st.session_state.current_block_index = 0
                st.session_state.view = 'card'
                nav.current_card_index = st.session_state.current_card_index
                nav.current_block_index = st.session_state.current_block_index
                nav.view = st.session_state.view
                st.rerun()

    return selected_card
