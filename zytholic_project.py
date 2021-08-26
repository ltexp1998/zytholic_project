import streamlit as st
import requests
#import api
#import uvicorn


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

st.write(
    '<style>div.row-widget.stRadio> div{display: flex; flex-flow: row; justify-content: center;}</style>',
    unsafe_allow_html=True)

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

#Style Selection

st.markdown('<h2 class="border">Style Selection : (Choose one)</h2>',unsafe_allow_html=True)

style = st.radio("", ["Stout", "Sour", "IPA"])

# Taste Selection

st.markdown('    ')

st.markdown('<h2 class="border">Taste Selection : (Choose one)</h2>',unsafe_allow_html=True)

taste = st.radio("",["Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar"])

st.markdown('    ')

st.markdown('    ')

# ABV and IBU bar select

#option_ABV = st.slider('ABV : %/Vol', 0, 60, 1)
option_IBU = st.slider('IBU : ', 0, 100, 1)

st.markdown('<h2 class="border2">Style proposition :</h2>', unsafe_allow_html=True)

# enter here the address of api

# test de l'endpoint "test" de l'API
# option_ABV = int(st.sidebar.slider('ABV : %/Vol', 0, 60, 1))
# urltest = (f'http://localhost:2809/test?test={option_ABV}')
# response = requests.get(urltest).json()[0]
# st.sidebar.markdown(response)

# test de l'endpoint "10_prefered_beers" de l'API
url_ten_beer = (f'http://localhost:2809/10_prefered_beers?style={style}')
response = requests.get(url_ten_beer).json()[0]
st.sidebar.markdown(style)

# test de l'endpoint "taste" de l'API
url_taste = (f'http://localhost:2809/taste?taste={taste}')
response = requests.get(url_taste).json()[0]
st.sidebar.markdown(response)

# test de l'endpoint "brewery" de l'API
# url_brewery = (f'http://localhost:2809/taste?taste={brewery}')
# response = requests.get(url_brewery)
# st.sidebar.markdown(brewery)
