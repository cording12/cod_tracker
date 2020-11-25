def html_custom_title(usr_string):
    html_title = f"""
    <style>
    .title h1{{
      # user-select: none;
      font-size: 50px;
      font-family: Segoe UI;
      color: black;
      # background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
      # background-size: 600vw 600vw;
      # -webkit-text-fill-color: transparent;
      # -webkit-background-clip: text;
      # animation: slide 10s linear infinite forwards;
    }}
    # @keyframes slide {{
    #   0%{{
    #     background-position-x: 0%;
    #   }}
    #   100%{{
    #     background-position-x: 600vw;
    #   }}
    # }}
    </style>
    
    <div class="title">
        <h1>{usr_string}</h1>
    </div>
    """
    return html_title


def assign_id(div_id):
    col_bg = f"""
    <div class ={div_id}
    </div>
    """
    return col_bg


def set_background_image_fill_overlay(div_class, img_url):
    item_bg = f"""
        <style>
        .{div_class}{{
            height: 180px;
            overflow: hidden;
            background-size: cover;
            background-position: center;
            background-image: 
                repeating-linear-gradient(rgba(0, 0, 0,0.6), rgba(0, 0, 0, 0.6)),
                url({img_url});
        }}
        </style>                                
    """
    return item_bg
