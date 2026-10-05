import streamlit as st

def style_background_home():
    st.markdown("""
    <style>
        .stApp {
            background: #5865F2 !important;
        }
        .stApp div[data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 2.5rem !important;
            border-radius: 2rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("""
    <style>
        .stApp {
            background: #E0E3FF !important;
        }
    </style>
    """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        .block-container {
            padding-top: 1.5rem !important;
        }

        html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, div, span, label, button, input {
            font-family: 'Outfit', sans-serif !important;
        }

        h1 {
            font-weight: 800 !important;
            font-size: 2.2rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }

        h2 {
            font-weight: 700 !important;
            font-size: 1.8rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }

        h3, h4, p {
            font-weight: 500 !important;
        }

        .stButton > button {
            border-radius: 1.2rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 8px 18px !important;
            border: none !important;
            transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out !important;
        }

        .stButton > button[kind="secondary"] {
            border-radius: 1.2rem !important;
            background-color: #EB459E !important;
            color: white !important;
            padding: 8px 18px !important;
            border: none !important;
        }

        .stButton > button[kind="tertiary"] {
            border-radius: 1.2rem !important;
            background-color: #23272A !important;
            color: white !important;
            padding: 8px 18px !important;
            border: none !important;
        }

        .stButton > button:hover {
            transform: scale(1.03) !important;
        }
    </style>
    """, unsafe_allow_html=True)