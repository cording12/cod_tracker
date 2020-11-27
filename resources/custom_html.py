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


def custom_table(h1, h2, h3,
                 map1, map2, map3,
                 map1k, map2k, map3k,
                 map1kd, map2kd, map3kd):
    # Easy table HTMLgenerator
    # https://www.tablesgenerator.com/html_tables
    table = f"""
    <style type="text/css">
    .tg  {{border-collapse:collapse;border-color:#ccc;border-spacing:0;}}
    .tg td{{background-color:#fff;border-bottom-width:1px;border-color:#ccc;border-style:solid;border-top-width:1px;
      border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding: 5px 5px;
      word-break:normal;}}
    .tg th{{background-color:#f0f0f0;border-bottom-width:1px;border-color:#ccc;border-style:solid;border-top-width:1px;
      border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;
      padding:5px 5px;word-break:normal;}}
    .tg .tg-fymr{{border-color:inherit;font-weight:bold;text-align:left;vertical-align:top;white-space:nowrap}}
    .tg .tg-btxf{{background-color:#f9f9f9;border-color:inherit;text-align:left;vertical-align:top;white-space:nowrap}}
    .tg .tg-0pky{{border-color:inherit;text-align:left;vertical-align:top;white-space:nowrap}}
    .tg{{width:100%}}
    
    </style>
    <table class="tg">
    <thead>
      <tr>
        <th class="tg-fymr">{h1}</th>
        <th class="tg-fymr">{h2}</th>
        <th class="tg-fymr">{h3}</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-btxf">{map1}</td>
        <td class="tg-btxf">{map1k}</td>
        <td class="tg-btxf">{map1kd}</td>
      </tr>
      <tr>
        <td class="tg-0pky">{map2}</td>
        <td class="tg-0pky">{map2k}</td>
        <td class="tg-0pky">{map2kd}</td>
      </tr>
      <tr>
        <td class="tg-btxf">{map3}</td>
        <td class="tg-btxf">{map3k}</td>
        <td class="tg-btxf">{map3kd}</td>
      </tr>
    </tbody>
    </table>

    """
    return table
