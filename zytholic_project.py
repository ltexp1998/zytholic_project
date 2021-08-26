import streamlit as st
import requests
#import api
#import uvicorn

# CSS

st.markdown(""" <style>
#zytholic-project {text-align: center; font-size: 4em; text-transform: uppercase;}
</style> """, unsafe_allow_html=True)

st.markdown(""" <style>
#help-yourself-to-discover-new-beer {text-align: center;font-size: 2em; padding-bottom: 2em;text-transform: capitalize;}
</style> """, unsafe_allow_html=True)

st.markdown(""" <style>
.border { border : solid black 1px;
padding : 0.5em }
</style> """, unsafe_allow_html=True)

st.markdown(""" <style>
#style-proposition { border : solid black 1px;
padding: 0.5em;
padding-bottom : 25em}
</style> """, unsafe_allow_html=True)

st.write(
    '<style>div.row-widget.stRadio> div{display: flex; flex-flow: row; justify-content: center;}</style>',
    unsafe_allow_html=True)

# Site title

"""# zytholic project"""

"""## help yourself to discover new beer"""


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

style = st.selectbox("Style list", ["","Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA","Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA"])

# Taste Selection

st.markdown('    ')

st.markdown('<h2 class="border">Taste Selection : (Choose one)</h2>',unsafe_allow_html=True)

taste = st.selectbox("Taste list", ["","Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar", "Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar"])


st.markdown('    ')

st.markdown('    ')

# ABV and IBU bar select

option_ABV = st.slider('ABV : %/Vol', 0, 60, 1)
st.markdown('    ')

option_IBU = st.slider('IBU : ', 0, 100, 1)
st.markdown('    ')

st.markdown('<h2 class="border2">Style proposition :</h2>', unsafe_allow_html=True)

# enter here the address of api

url_local = 'http://localhost:2809'
#url_distant = 'https://add_of_the_provider'

# test de l'endpoint "test" de l'API

urltest = (f'{url_local}/test?test={option_ABV}')
response = requests.get(urltest).json()[0]
st.sidebar.markdown(f'test : {response}')


# test de l'endpoint "10_prefered_beers" de l'API
url_ten_beer = (f'{url_local}/10_prefered_beers?style={style}')
beer_result = requests.get(url_ten_beer).json()[0]
st.sidebar.markdown(f'style : {beer_result}')

# test de l'endpoint "taste" de l'API
url_taste = (f'{url_local}/taste?taste={taste}')
taste_result = requests.get(url_taste).json()[0]
st.sidebar.markdown(f'taste : {taste_result}')

# test de l'endpoint "brewery" de l'API
# url_brewery = (f'{url_local}/taste?taste={brewery}')
# response = requests.get(url_brewery)
# st.sidebar.markdown(brewery)
