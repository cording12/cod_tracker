"""This configures the CSS for the custom theme"""

dark_c = "#313a46" # Sidebar background colour
grey_c = "#F9FAFD" # Page background colour
grey_c_text = "#8391a2" # Sidebar text colour
H4_text = "#6c757d" # Dark grey

def sidebar_format():
    ret = """
    <style>
    .sidebar .sidebar-content {
        background-color: #313a46;
        background-image: linear-gradient(#313a46, #313a46);
        color: #8391a2;
    }
    </style>
    """
    return ret


def page_format():
    ret = """
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@200;400;600;700;900&display=swap" rel="stylesheet">
 
    <style>
    body {
        background-color: #F5F5F5;
        font-family: Nunito Sans, sans-serif;
        color: #98a6ad!important;
    }
       
    .reportview-container .markdown-text-container{
        font-family: Nunito Sans, sans-serif;
    }       
    
    h4{
        font-family: Nunito,sans-serif;
        color:#6c757d;
        text-transform:uppercase;
        letter-spacing: .02em;
        font-size:.9rem;
        margin-bottom:1.5rem!important;
    }
    
    </style>
    """
    return ret


def block_format():
    # box-shadow:0 0 35px 0 rgba(154,161,171,.15);
    # stBlock - horiz
    ret = """
    <style>
    .stBlock{
        background-color: white;
        padding:1rem;
        padding-top:0;
        padding-bottom:.2rem;
        border-radius: .25rem;
        # box-shadow:0 0 35px 0 rgba(154,161,171,.15);
    }
    .stBlock-horiz{
        background-color: white;
        margin-left:-1rem;
        margin-right:-1rem;
        box-shadow:0 0 0px 0 rgba(0,0,0,0);
    }
    
    .stBlock.st-et.st-er.st-eu{
        box-shadow:0 0 0px 0 rgba(0,0,0,0);    
    }
    </style>
    """
    return ret


# def block_format():
#     # box-shadow:0 0 35px 0 rgba(154,161,171,.15);
#     # stBlock - horiz
#     ret = """
#     <style>
#     .stBlock{
#         background-color: white;
#         padding:1rem;
#         padding-top:0;
#         padding-bottom:.2rem;
#         border-radius: .25rem;
#     }
#     </style>
#     """
#     return ret