import streamlit as st
import requests


"""# Zytholic_project web site"""

# CSS

st.markdown(""" <style>
.border { border : solid black 2px;
padding : 0.5em }
</style> """, unsafe_allow_html=True)

st.markdown(""" <style>
.border2 { border : solid white 1px;
padding: 0.5em;
padding-bottom : 25em}
</style> """, unsafe_allow_html=True)

# SIDE BAR

st.sidebar.markdown(f"""
    # Legend :
    """)

st.sidebar.markdown(f"""
    ## ABV :
    """)

st.sidebar.markdown(f"""
    ### Alcohol by Volume. You know this one! Turns out how much alcohol in a beer really matters for style!
    """)

st.sidebar.markdown(f"""
    ## IBU :
    """)

st.sidebar.markdown(f"""
    ### International Bittering Units. How bitter is this beer?
    ### 0 water to 100+ super bitter.
    """)

# enter here the address of api
url = 'http://localhost:8501'

response = requests.get(url, '/test')

st.sidebar.markdown(response)

#Style Selection

st.markdown('<h2 class="border">Style Selection :</h2>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.checkbox('Stout')
col2.checkbox('Sour')
col3.checkbox('IPA')
col1.checkbox('Goze')
col2.checkbox('Lager')
col3.checkbox('NEIPA')
col1.checkbox('Porter')
col2.checkbox('Pils')
col3.checkbox('Wheat')

# Taste Selection

st.markdown('    ')

st.markdown('<h2 class="border">Taste Selection :</h2>',
            unsafe_allow_html=True)

col1_2, col2_2, col3_2 = st.columns(3)

col1_2.checkbox('Fruit')
col2_2.checkbox('Malty')
col3_2.checkbox('Hoppy')
col1_2.checkbox('Bitter')
col2_2.checkbox('Sweet')
col3_2.checkbox('Salty')

st.markdown('    ')

st.markdown('    ')
# ABV and IBU bar select

option_ABV = st.slider('ABV : %/Vol', 0, 60, 1)
option_IBU = st.slider('IBU : ', 0, 100, 1)

st.markdown('<h2 class="border2">Style proposition :</h2>', unsafe_allow_html=True)
