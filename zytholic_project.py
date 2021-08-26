import streamlit as st
import requests

st.markdown(""" <style>
#style-proposition { border : solid black 1px;
padding: 0.5em;
padding-bottom : 25em}
</style> """, unsafe_allow_html=True)

st.write(
    '<style>div.row-widget.stRadio> div{display: flex; flex-flow: row; justify-content: center;}</style>',
    unsafe_allow_html=True)

# Site title

st.markdown('<h1 style="text-align: center; font-size: 4em; text-transform: uppercase;">zytholic project</h1>', unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center;font-size: 2em; padding-bottom: 2em;text-transform: capitalize;">help yourself to discover new beer</h2>', unsafe_allow_html=True)

# SIDE BAR

# how to use the app
st.sidebar.markdown('<h2 style="text-align: center; text-transform: uppercase; text-decoration: underline; color:purple">To use the app : </h2>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-weight: bold; text-decoration: underline;">Complite ONE of these feature :</div>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="padding-top: 1em">Enter the name of a beer</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p ><span style="font-weight: bold;">OR</span> Choose a Style (ex : IPA)</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p ><span style="font-weight: bold;">OR</span> Choose a Taste (ex : Hoppy)</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p ><span style="font-weight: bold;">OR</span> Choose ABV or IBU</p>', unsafe_allow_html=True)

#legend
st.sidebar.markdown('<h2 style="text-align: center; text-transform: uppercase; text-decoration: underline; color:purple">legend : </h2>', unsafe_allow_html=True)

st.sidebar.markdown(f"""## ABV :""")
st.sidebar.markdown(f"""
                    ## Alcohol by Volume. You know this one !
                    ## Turns out how much alcohol in a beer really matters for style!
                    """) #NE PAS MODIFIER LES RENVOIS DE LIGNE !!!!
st.sidebar.markdown(f"""## IBU :""")

st.sidebar.markdown(f"""
    ## International Bittering Units. How bitter is this beer?
    ## 0 water to 100+ super bitter.
    """)  #NE PAS MODIFIER LES RENVOIS DE LIGNE !!!!

st.sidebar.markdown(f"""
    # Test du retour de l'API en mode "dummy"
    """)

#Name of a beer

st.markdown('<h2 style=" border : solid black 1px; padding : 0.5em ">Enter the name of a beer you like :</h2>',unsafe_allow_html=True)

beer_name = st.text_input('', '')

st.markdown('    ')

#Style Selection

st.markdown('<h2 style=" border : solid black 1px; padding : 0.5em ">Style Selection : (Choose one)</h2>',unsafe_allow_html=True)

style = st.selectbox("", ["Make your style here","Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA","Stout", "Sour", "IPA", "Stout", "Sour", "IPA", "Stout", "Sour", "IPA"])

# Taste Selection

st.markdown('    ')

st.markdown('<h2 style=" border : solid black 1px; padding : 0.5em ">Taste Selection : (Choose one)</h2>',unsafe_allow_html=True)

taste = st.selectbox("", ["Make your taste here","Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar", "Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar"])


st.markdown('    ')

st.markdown('    ')

# ABV and IBU bar select

option_ABV = st.slider('ABV : %/Vol', 0, 60, 1)
st.markdown('    ')

option_IBU = st.slider('IBU : ', 0, 100, 1)
st.markdown('    ')

st.markdown('<h2 class="border2">Style proposition :</h2>', unsafe_allow_html=True)

# enter here the address of api

#url_local = 'http://localhost:2809'
#url_distant = 'http://localhost:5000'
url_distant = 'https://api-zytholic-project-uq4l4l4m7a-ew.a.run.app'
# test de l'endpoint "test" de l'API

urltest = (f'{url_distant}/test?test={option_ABV}')
response = requests.get(urltest).json()[0]
st.sidebar.markdown(f'test : {response}')


# test de l'endpoint "10_prefered_beers" de l'API
url_ten_beer = (f'{url_distant}/10_prefered_beers?style={style}')
beer_result = requests.get(url_ten_beer).json()[0]
st.sidebar.markdown(f'style : {beer_result}')

# test de l'endpoint "taste" de l'API
url_taste = (f'{url_distant}/taste?taste={taste}')
taste_result = requests.get(url_taste).json()[0]
st.sidebar.markdown(f'taste : {taste_result}')

# test de l'endpoint "brewery" de l'API
# url_brewery = (f'{url_local}/taste?taste={brewery}')
# response = requests.get(url_brewery)
# st.sidebar.markdown(brewery)
