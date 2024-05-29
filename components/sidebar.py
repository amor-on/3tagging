import streamlit as st

def render_sidebar(nav):
    st.sidebar.title('Selector de Tarjetas')
    card_titles = nav.get_card_titles()
    selected_card = st.sidebar.selectbox('Seleccionar Tarjeta', card_titles, index=st.session_state.current_card_index)
    if selected_card != nav.get_current_card():
        st.session_state.current_card_index = card_titles.index(selected_card)
        st.session_state.current_block_index = 0
        st.session_state.view = 'card'
        nav.current_card_index = st.session_state.current_card_index
        nav.current_block_index = st.session_state.current_block_index
        nav.view = st.session_state.view
    return selected_card
