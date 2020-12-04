"""This configures the CSS for the custom theme"""
import streamlit as st

hero_img_desktop = "https://www.callofduty.com/content/dam/atvi/callofduty/cod-touchui/zeus/home/hero/hero-key-art-zeus-desktop.jpg"
hero_img_mobile = "https://www.callofduty.com/content/dam/atvi/callofduty/cod-touchui/zeus/home/hero/hero-key-art-zeus-mobile.jpg"

colour_body_text = "#98a6ad"
colour_dark_blue_sidebar_bg = "#313a46"  # Sidebar background colour
colour_dark_grey_text = "#6c757d"  # Dark grey
colour_mid_grey_sidebar = "#8391a2"  # Sidebar text colour
colour_page_background = "#EFEFEF"
colour_white = "white"

font_master = "Nunito Sans, sans-serif"

test_colour = "coral"


def local_css(file_name):
    """
    Loads an external CSS file
    :param file_name: name of the CSS file including extension
    :return: opens css file
    """
    with open("static/css/" + file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def bootstrap_css():
    """Loads the bootstrap CSS into the page"""
    cssload = """
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" 
    integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" 
    crossorigin="anonymous">
    """
    return cssload


def sidebar_format():
    ret = f"""
    <style>
    .sidebar .sidebar-content {{
        background-color: {colour_dark_blue_sidebar_bg};
        background-image: linear-gradient({colour_dark_blue_sidebar_bg}, {colour_dark_blue_sidebar_bg});
        color: {colour_mid_grey_sidebar}!important;
    }}
    </style>
    """
    return ret


def page_format():
    # Body was F5F5F5
    ret = f"""
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@200;400;600;700;900&display=swap" rel="stylesheet">
 
    <style>
    
    body {{
        background-color: {colour_page_background};
        font-family: {font_master};
        color: {colour_body_text}!important;
    }}
       
    .reportview-container .markdown-text-container{{
        font-family: {font_master};
    }}       
    
    h4{{
        color:{colour_dark_grey_text};
        text-transform:uppercase;
        letter-spacing: .02em;
        font-size:.9rem;
        margin-top:.5rem!important;
        margin-bottom:1.5rem!important;
    }}

    </style>
    """
    return ret


def block_format():
    # box-shadow:0 0 35px 0 rgba(154,161,171,.15);
    ret = f"""
    <style>

    .stBlock{{
        background-color: {colour_white};
        padding:1rem;
        padding-top:0;
        padding-bottom:.2rem;
        border-radius: .25rem;
        # box-shadow:0 0 35px 0 rgba(154,161,171,.15);
        margin-top:2rem;
    }}
    .stBlock-horiz{{
        background-color: {colour_white};
        margin-left:-1rem;
        margin-right:-1rem;
        box-shadow:0 0 0px 0 rgba(0,0,0,0)!important;
    }}

    .stAlert{{
        letter-spacing: .02em;
    }}
    
    .Widget>label{{
        color:inherit;
    }}

    .StatusWidget-enter-done .ReportStatus{{
        background-color:inherit;
    }}
    
    .stRadio div label div{{
        color:inherit;
    }}
    
    .stRadio div label{{
        background-color:inherit;
    }}
    
    .stCheckbox label div{{
        color:inherit;
    }}
    
    .stCheckbox label{{
        background-color:inherit;
    }}

    #ReportStatus {{
        background-color:inherit;
    }}

    .streamlit-expander li div{{
        font-family:{font_master};
        color:inherit;
    }}

    </style>
    """
    return ret


def hero(plyr, pltf):
    ret = f"""
    <div class="heroImage">
        <div class="heroContents">
            <h1 style=padding-bottom:0.2rem>Call of Duty: Cold War</h1>
            <p>Showing player data for {plyr} on {pltf}.</p>
        </div>
    </div>

    <style>
    .heroImage {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.9)), 
        url("{hero_img_desktop}");
        height: 25vh;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
        border-radius: .25rem;
        margin-bottom:2rem;
        margin-top:-5vh;
    }}

    .heroContents{{
        display:flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        padding-left: 2rem;
        padding-right: 1rem;
        color: {colour_white};
    }}

    </style>

    
    """
    return ret