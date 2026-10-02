import streamlit as st


def footer_home():
    logo_url = "Fighters.png"
    
    st.markdown(f""" 
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:white;" > Created By Fighters </p>
        <img src='{logo_url}' style='height:100px;' />
        </div>
                """, unsafe_allow_html=True)