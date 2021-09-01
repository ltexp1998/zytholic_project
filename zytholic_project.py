import streamlit as st
import requests
import base64
import pandas as pd


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
    background-image : url("data:image/png;base64,%s");
    background-size : cover;
    background-color : rgba(0,0,255,0.3)
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./assets/img/beer.png')

################# BACKGROUND IMAGE CREDIT ON HTML #################

st.markdown('<p style="visibility : hidden">Image credit : https://urlz.fr/gm4x"</p>', unsafe_allow_html=True)

################# CSS custom section #################

CSS = """
.reportview-container {background : rgba(0, 0, 0, 0.6);}
.stSlider, .css-1iyw2u1, .css-1djdyxw{color : white;}
.css-2y0inq, .css-1d0tddh  {color : white}

div[role="listbox"] ul {background-color :black;}
div[role="radiogroup"] {flex-flow : row; justify-content : center; }
div[role="radiogroup"]  .st-cc {font-size : 2em; color : white;}
.st-bw, .st-cb{font-size : 1.5em;}
.css-1ekf893 a {text-decoration : none; color : yellow; display : flex; text-align : center;}
div[data-testid="stThumbValue"] {font-size : 1.5em; padding-bottom : 1em}
div[data-testid="stTickBarMin"] {font-size : 1.5em}
div[data-testid="stTickBarMax"] {font-size : 1.5em}
div[data-baseweb="base-input"] .st-dg {font-size : 2em}
div[data-baseweb="select"] .st-el {font-size : 2em}
.css-2y0inq, .css-1d0tddh, .st-ed{font-size : 2em}

.api_return {font-weight: bold; color : white; font-size : 1.2em}
.border2 {color : white; padding : 0.5em}
.beer_name_api_call {font-weight: bold; color : white; font-size:1.5em;}
.beer_name_api_return {font-weight: bold; color : white; font-size : 3em; display : flex; text-align : center; justify-content : center;}
.link_BA {margin : -1.5em; display : flex; justify-content : center;}
.prop_degust {color : white; padding : 0.5em; text-align : center; font-size : 1.8em;text-decoration : underline}
.prop_degust_title {color : white; padding : 0.5em; font-size : 2em; text-align : center;}
.repeat_choice {color : white; padding : 0.5em; text-align : center; border : 1.5px solid white; font-size : 2em}
.return_link {justify-content: center; margin-top : -0.5em}
.return_title {font-weight: bold; color : white; font-size : 1.5em; display : flex; justify-content : center;}
.suggestion_return_1 {margin-bottom: -1.5em;color : white;font-size : 1em; text-transform : capitalize;font-size : 1em;}
.suggestion_return_2 {color : white;font-size : 1em; text-transform : capitalize;font-size : 1em; border-bottom : 2px solid white; padding-bottom : 1em}
.select_title {color : white; padding : 0.5em; font-size : 2.5em}
.slide_title {color : white; margin-bottom : -2em; font-size : 1.5em}
.title1 {color : white; text-align : center; font-size : 4em; text-transform : uppercase;}
.title2 {color : white; text-align : center;font-size : 2em; padding-bottom : 1em;text-transform : capitalize;}

.side_bar_use_app {text-align : center; text-transform : uppercase; text-decoration : underline; color :purple}
.side_bar_bold_underline {font-weight : bold; text-decoration : underline;}
.side_bar_bold {font-weight : bold;}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

################# SIDE BAR #################

# how to use the app

st.sidebar.markdown('<h2 class="side_bar_use_app">How to use the app : </h2>',
                    unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="side_bar_bold_underline">Complite ONE of these feature :</div>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<p style="padding-top : 1em"><span class="side_bar_bold">Enter</span> the name of a beer</p>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<p><span class="side_bar_bold">OR</span> Choose a Style (ex : IPA)</p>',
    unsafe_allow_html=True)
# st.sidebar.markdown(
#     '<p><span class="side_bar_bold">OR</span> Choose a Taste (ex : Hoppy)</p>',
#     unsafe_allow_html=True)

st.sidebar.markdown('<p><span class="side_bar_bold">AND</span> Choose ABV or IBU</p>',
                    unsafe_allow_html=True)

#legend section

st.sidebar.markdown('<h2 class="side_bar_use_app">legend : </h2>',
                    unsafe_allow_html=True)

st.sidebar.markdown("""## ABV :""")
st.sidebar.markdown("""Alcohol by Volume. You know this one !
Turns out how much alcohol in a beer really matters !""")  # DO NOT MODIFY ENDENTATION AND LINE RETURN !!!!

st.sidebar.markdown("""## IBU :""")
st.sidebar.markdown("""International Bittering Units.

How bitter is this beer ?
### _from :_ ***0 IBU like water***
### _to :_ ***100 IBU super bitter.***
""")  # DO NOT MODIFY ENDENTATION AND LINE RETURN !!!!

################# SITE TITLE section #################

st.markdown('<h1 class="title1">zytholic project</h1>', unsafe_allow_html=True)

st.markdown('<h2 class="title2">help yourself to discover new beer</h2>', unsafe_allow_html=True)

################# MAIN PAGE #################

# FEATURE SELECTION : checkbox with feature selection

st.markdown('<h2 class="title2">Feature selection</h2>', unsafe_allow_html=True)
feature = st.radio('', ('Name', 'Style'))

# if the feature Taste available :
# feature = st.radio('', ('Name', 'Style', 'Taste'))

st.markdown('    ')
st.markdown('    ')


# NAME OF A BEER field section

if feature == 'Name':
    st.markdown('<h2 class="select_title">Enter the name of a beer :</h2>',unsafe_allow_html=True)
    # return the beer's name with all entry capitalize to match with the dataset :
    beer_name = st.text_input('', '').title()

# STYLE SELECTION section

elif feature == 'Style':
    st.markdown('<h2 class="select_title">Style Selection : (Choose one)</h2>',unsafe_allow_html=True)

    if st.checkbox('Click here to "special" style (like : Barleywine or Rye)'):
        style = st.selectbox("", [
            "Lambic", 'Lambic', 'Smoked', 'Rye', 'Barleywine', 'Bitter',
            'Brett', 'Altbier', 'Dubbel', 'Steam Beer', 'NEIPA', 'Ale Old',
            'Bière de Garde', 'Quadrupel', 'Tripel', 'Saison', 'Braggot',
            'Happoshu', 'Herb and Spice Beer', 'Pumpkin Beer', 'Kölsch',
            'Bière de Champagne / Bière Brut', 'Sahti', 'Rice',
            'Winter Warmer', 'Kvass', 'Fruit and Field Beer',
            'Low Alcohol Beer'
        ])

    else :
        style = st.selectbox("", [
            "Lager", 'Lager', 'Stout', 'Ale', 'Wheat', 'IPA', 'Ale Dark',
            'Bock', 'Porter', 'Sour', 'Ale Strong', 'Ale Pale', 'Ale Red',
            'Pilsner'
        ])

# TASTE SELECTION section

# elif feature == 'Taste':
#     st.markdown('<h2 class="select_title">Taste Selection : (Choose one)</h2>',unsafe_allow_html=True)

#     taste = st.selectbox("", ["Choose your taste here","Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar", "Fruit", "Malty", "Hoppy", "Salty", "Bitter", "Sweet", "Sugar"])

st.markdown('    ')
st.markdown('    ')

# ABV and IBU SLIDEBAR section

st.markdown('<p class="slide_title">ABV : %/Vol</p>', unsafe_allow_html=True)
option_ABV = st.slider('', min_value=0., max_value=20., value=8., step=0.1)
st.markdown('<p class="slide_title">IBU :</p>', unsafe_allow_html=True)
option_IBU = st.slider('', min_value = 0, max_value = 100, value = 50, step = 1)

################# API CALL #################

# enter here the address of api

url_local = 'http://localhost:1234'
url_docker = 'http://0.0.0.0:5000'
url_distant = 'https://api-zytholic-project-uq4l4l4m7a-ew.a.run.app'

################# API BEER NAME #################

if feature == 'Name':
    API_call_name = (
        f'{url_distant}/filter_abv_ibu?name={beer_name}&abv={option_ABV}&ibu={option_IBU}'
    )
    response = requests.get(API_call_name).json()

################# API STYLE #################

if feature == 'Style':

    API_call_style = (
        f'{url_distant}/style_search?style={style}&abv={option_ABV}&ibu={option_IBU}'
    )
    response = requests.get(API_call_style).json()

################# TEST format réponse à supprimer #################

#st.sidebar.markdown(f'test : {response}')

################# suggestion SELECTION section #################

if feature == "Style":
    st.markdown(
        '<h2 class="repeat_choice">'
        f'Your Style\'s choice is : <span class="beer_name_api_call">{style}</span>'
        '</h2>',
        unsafe_allow_html=True)

for key, value in response.items():
    result_json = value
    execpt_result = key

if key == 'response':

    st.markdown(
        '<h2 class="repeat_choice">'
        f'The Beer : <span class="beer_name_api_call">{beer_name}</span></br></br>Doesn\'t exist in the database'
        '</h2>',
        unsafe_allow_html=True)
else:
    if feature =="Name":
        st.markdown(
            '<h2 class="repeat_choice">'
            f'Your Beer name\'s choice was :</br><span class="return_title">{beer_name}</span></br><a class="return_link" href="https://www.beeradvocate.com/search/?q={beer_name}" target="_blank"> ( Beer info : &#127866;)</a>'
            '</h2>',
            unsafe_allow_html=True)
    st.markdown(
        '<h2 class="prop_degust_title">Tasting suggestion :</h2>',
        unsafe_allow_html=True)
    prop = 0
    for i in value:
        choice = response['name'][i]
        name = response['name'][i]
        brewery = response['brewery'][i]
        abv = response['abv'][i]
        style = response['style'][i]
        ibu = (int(response['min ibu'][i]) + int(response['max ibu'][i])) / 2

        if prop == 0 :
            pass
        if prop > 0 :
            st.markdown(
                '<p class = "suggestion_return_1">'
                f'<span class="prop_degust">suggestion {prop}</span> : </br><span class="beer_name_api_return">{name}</span></br><a class="link_BA" href="https://www.beeradvocate.com/search/?q={name} {brewery}" target="_blank"> ( Beer info : &#127866;)</a></br><span class="api_return">{abv}°</span> alc </br> style : <span class="api_return">{style}</span> </br> made by brewery : <span class="api_return">{brewery}</span>'
                '</p>'
                '</br>'
                '<p class = "suggestion_return_2">'
                f'Mean IBU : <span class="api_return">{ibu}</span>'
                '</p>',
                unsafe_allow_html=True)
        prop += 1

################# TEST RETOUR DATAFRAME PANDAS #################

#st.write(pd.DataFrame(response)) # test non concluant
