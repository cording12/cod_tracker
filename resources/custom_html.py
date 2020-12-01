"""Contains the HTML formatting functions"""


def assign_id(div_id):
    """Give an ID to the specified div"""
    col_bg = f"""
    <div class ={div_id}
    </div>
    """
    return col_bg


def set_background_image_fill_overlay(div_class, img_url):
    """Add background image and formatting to the specified element based on div class"""
    item_bg = f"""
        <style>
        .{div_class}{{
            height: 250px;
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
    """Draws and formats HTML tables with content values passed through the function variables
    Easy table HTMLgenerator: https://www.tablesgenerator.com/html_tables
    """

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


def central_col_size_adjust(div_class, width_calc):
    """Adjusts the formatting of the central column"""
    padding_cal = 100 - width_calc
    padding_ttl = (padding_cal / 2) / 2
    col_size = f"""
        <style>
        .{div_class}{{
            margin:0 auto;
            padding-right: {padding_ttl}%;
            padding-left: {padding_ttl}%;
        }}
        </style>                                
    """
    return col_size


def format_para_size(rem_size, usrstr):
    """
    HTML to format the P tag as specified by the user
    :param rem_size:  Desired font size entered by user
    :param usrstr: Desired string entered by user
    :return: string html
    """
    shrink_text = f"""       
    <p style="font-size:{rem_size}rem;margin-bottom:6.4px; margin-top:-10px">{usrstr}</p>
    """
    return shrink_text


def grid_layout_two(div_grid_id):
    grid_layout = f"""
    <style>
    .{div_grid_id}{{
        display:grid;
        grid-template-columns: 1fr 1fr;
        grid-gap: 1.5rem;
    }}
    """
    return grid_layout


def grid_test(col1, col2, col3, img_url=0):
    img_url = "https://www.callofduty.com/cdn/app/base-maps/cw/mp_tank.jpg"
    grid_layout = f"""
    <div class="container map_summary_container">
        <div class=" map_summary_heading">
            Best map by KD
        </div>
      <div class="row h-custom align-items-center">
        <div class="col-sm best_map_text">{col1}</div>
            <div class="col-sm">
                <div class="row">
                    <div class="col-sm">First row {col2}</div>
                    <div class="col-sm">First row {col3}</div>
                </div>
                <div class="row row_pad">
                    <div class="col-sm">Next row {col2}</div>
                    <div class="col-sm">Next row {col3}</div>
            </div>
      </div>
    </div>

    <style>
    .h-custom{{    
    height: 85%!important;
    }}
    </style>

    <style>
    .row_pad{{    
    padding-top: 20px;
    }}
    </style>

    <style>
    .map_summary_container{{    
    height: 250px;
    color:white;
    overflow: hidden;
    padding: .5rem 1.5rem 2rem;
    background-size: cover;
    background-position: center;
    background-image: 
        repeating-linear-gradient(rgba(0, 0, 0,0.6), rgba(0, 0, 0, 0.6)),
        url({img_url});
    }}
    </style>

    <style>
    .map_summary_heading{{    
    font-size:1.25em;
    font-family: Segoe UI;
    padding-top:0.5rem;
    margin:0;
    }}
    </style>

    <style>
    .best_map_text{{    
    font-size:1.5em;
    font-family: Segoe UI semibold;
    }}
    </style>
    """
    return grid_layout


def bootstrap_css():
    """Loads the bootstrap CSS into the page"""
    cssload = """
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" 
    integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" 
    crossorigin="anonymous">
    """
    return cssload


def custom_css():
    """Loads custom CSS into the page"""
    cssload = """
    <link rel="stylesheet" href="/static/css/new_theme.css">
    """
    return cssload


def accuracy_widget(avgacc, bestacc):
    ret = f"""
    <div class="accuracy_stats_container">
      <div class="row h-100 flex-column">
        <div class="col-sm small_header_text">
            Average accuracy
            <div class="hero_number_text">{avgacc}%</div>
        </div>
        <div class="col-sm small_header_text">
            Best accuracy
            <div class="hero_number_text">{bestacc}%</div>
        </div> 
      </div>
    </div>

    <style>
    
    .flex-column{{
        flex-direction:column!important;
        align-items: stretch;
        margin:15%;
    }}
    
    .accuracy_stats_container{{   
    height:320px;
    color:grey;
    overflow: hidden;
    padding: .5rem 1.5rem 2rem;
    background-size: cover;
    background-position: center;
    background-color: #f9f9fd;
    text-align:center;
    }}

    .hero_number_text{{    
    font-size:2em;
    color:#6c757d;
    font-weight:400!important;
    margin:0;
    }}

    .small_header_text{{
    font-size:1em;
    color: #98a6ad!important;
    margin: auto;
    }}
    </style>


    """
    return ret