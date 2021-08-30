import streamlit as st
import requests
import base64

################# BACKGROUND IMAGE section #################

# Function founded on the streamlit blog to have a local storage background image and available on https://github.com/streamlit/streamlit/issues/3073

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./assets/img/beer.png')

################# BACKGROUND IMAGE CREDIT ON HTML #################

st.markdown('<p style="visibility : hidden">Image credit : https://urlz.fr/gm4x"</p>', unsafe_allow_html=True)

################# CSS custom section #################

CSS = """
.stSlider, .css-1iyw2u1, .css-1djdyxw{text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; }
.css-2y0inq {color :white}
.css-1cu04ak {background-color: white}
.border2 {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; padding : 0.5em}
#style-proposition {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; border : solid white 1px; padding: 0.5em; padding-bottom : 25em}
.title1 {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; text-align: center; font-size: 4em; text-transform: uppercase;}
.title2 {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; text-align: center;font-size: 2em; padding-bottom: 1em;text-transform: capitalize;}
.proposition_return {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white;font-size: 1em; padding-bottom: 1em;text-transform: capitalize;}
.use_app {text-align: center; text-transform: uppercase; text-decoration: underline; color:purple}
.bold_underline {font-weight: bold; text-decoration: underline;}
.bold {font-weight: bold;}
.select_title {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff; color: white; border : solid white 1px; padding : 0.5em}
.slide_title {text-shadow: 0 0 3px #ff0000, 0 0 3px #0000ff ; color: white; margin-bottom: -2em}
div[role="radiogroup"]{flex-flow: row; justify-content: center;}
div[role="listbox"] ul {background-color :black;}
div[role="radiogroup"] {text-shadow: 0 0 3px white, 0 0 3px white;}
.css-1d0tddh {background: -webkit-linear-gradient(white, yellow);-webkit-background-clip: text;-webkit-text-fill-color: transparent;}
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

################# SITE TITLE section #################

st.markdown('<h1 class="title1">zytholic project</h1>', unsafe_allow_html=True)

st.markdown('<h2 class="title2">help yourself to discover new beer</h2>', unsafe_allow_html=True)

################# MAIN PAGE #################

# FEATURE SELECTION : checkbox with feature selection

st.markdown('<h2 class="title2">Feature selection</h2>', unsafe_allow_html=True)
feature = st.radio('', ('Name', 'Style', 'Taste'))
st.markdown('    ')
st.markdown('    ')


# NAME OF A BEER field section

if feature == 'Name':
    st.markdown('<h2 class="select_title">Enter the name of a beer :</h2>',unsafe_allow_html=True)

    beer_name = st.text_input('', '')

# STYLE SELECTION section

elif feature == 'Style':
    st.markdown('<h2 class="select_title">Style Selection : (Choose one)</h2>',unsafe_allow_html=True)

    if st.checkbox('Click here to "special" style (ex : Barleywine or Rye)'):
        style = st.selectbox("", [
            "Choose your style here", 'Lambic', 'Smoked', 'Rye', 'Barleywine',
            'Bitter', 'Brett', 'Altbier', 'Dubbel', 'Steam Beer', 'NEIPA',
            'Ale Old', 'Bière de Garde', 'Quadrupel', 'Tripel', 'Saison',
            'Braggot', 'Happoshu', 'Herb and Spice Beer', 'Pumpkin Beer', 'Kölsch','Bière de Champagne / Bière Brut', 'Sahti', 'Rice', 'Winter Warmer','Kvass', 'Fruit and Field Beer', 'Low Alcohol Beer'
        ])

    else :
        style = st.selectbox("", [
            "Choose your style here", 'Lager', 'Stout', 'Ale', 'Wheat', 'IPA',
            'Ale Dark', 'Bock', 'Porter', 'Sour', 'Ale Strong', 'Ale Pale',
            'Ale Red', 'Pilsner'
        ])

# TASTE SELECTION section

elif feature == 'Taste':
    st.markdown('<h2 class="select_title">Taste Selection : (Choose one)</h2>',unsafe_allow_html=True)

    taste = st.selectbox("", ["Choose your taste here","Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar", "Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar"])

st.markdown('    ')
st.markdown('    ')

# ABV and IBU SLIDEBAR section

st.markdown('<p class="slide_title">ABV : %/Vol</p>', unsafe_allow_html=True)
option_ABV = int(st.slider('', min_value=0., max_value=20., value=8., step=0.1))
st.markdown('<p class="slide_title">IBU :</p>', unsafe_allow_html=True)
option_IBU = st.slider('', min_value = 0, max_value = 100, value = 50, step = 1)

################# API CALL #################

# enter here the address of api

#url_local = 'http://localhost:2809'
#url_distant = 'http://localhost:5000'
url_distant = 'https://api-zytholic-project-uq4l4l4m7a-ew.a.run.app'

# TEST DU RETOUR API A SUPPRIMER

# test de l'endpoint "test" de l'API

# urltest = (f'{url_distant}/test?test={option_ABV}')
# response = requests.get(urltest)
# st.sidebar.markdown(f'test : {response}')

# test de l'endpoint "10_prefered_beers" de l'API
# url_ten_beer = (f'{url_distant}/10_prefered_beers?style={style}')
# beer_result = requests.get(url_ten_beer).json()[0]
# st.sidebar.markdown(f'style : {beer_result}')

# test de l'endpoint "taste" de l'API
# url_taste = (f'{url_distant}/taste?taste={taste}')
# taste_result = requests.get(url_taste).json()[0]
# st.sidebar.markdown(f'taste : {taste_result}')



################# PROPOSITION SELECTION section #################

st.markdown('<h2 class="border2">Proposition with your previous choice :</h2>', unsafe_allow_html=True)

brewery = 'test_brewery'
name = 'test_name'
ABV_return = option_ABV
style = 'test_style'


st.markdown('<p class = "proposition_return">'f'{name} from {brewery} with {ABV_return}°alc and style : {style}''</p>, ',
            unsafe_allow_html=True)

################# SIDE BAR #################

# how to use the app

st.sidebar.markdown('<h2 class="use_app">To use the app : </h2>',
                    unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="bold_underline">Complite ONE of these feature :</div>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<p style="padding-top: 1em"><span class="bold">Enter</span> the name of a beer</p>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<p><span class="bold">OR</span> Choose a Style (ex : IPA)</p>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<p><span class="bold">OR</span> Choose a Taste (ex : Hoppy)</p>',
    unsafe_allow_html=True)

st.sidebar.markdown('<p><span class="bold">AND</span> Choose ABV or IBU</p>',
                    unsafe_allow_html=True)

#legend section

st.sidebar.markdown('<h2 class="use_app">legend : </h2>',
                    unsafe_allow_html=True)

st.sidebar.markdown(f"""## ABV :""")
st.sidebar.markdown(f"""
                    ## Alcohol by Volume. You know this one !
                    ## Turns out how much alcohol in a beer really matters for style!
                    """)  # DO NOT MODIFY ENDENTATION AND LINE RETURN !!!!

st.sidebar.markdown(f"""## IBU :""")
st.sidebar.markdown(f"""
    ## International Bittering Units. How bitter is this beer?
    ## 0 water to 100+ super bitter.
    """)  # DO NOT MODIFY ENDENTATION AND LINE RETURN !!!!
