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


def st_info_custom(textstr, urlstr="", url=""):
    ret = f"""
    
    <div class="stalert_custom_format">
        <p style="margin:.25rem 0;">
            <a href="{url}" class=custom_url>{urlstr}</a>
                {textstr}
        </p>
    </div>

    <style>

    .custom_url{{
        color: white!important;
        font-weight: 600!important;
        text-decoration: underline;
    }}

    .stalert_custom_format{{
        border-radius:.25rem;
        padding: 1rem;
        background-color: #394C5F;
        color: white;
    }}
    
    </style>

    """
    return ret


def data_widget_master_css():
    ret = f"""
    <style>

    .flex-column{{
        flex-direction:column!important;
        align-items: stretch;
        margin:5%;
    }}

    .data_widget{{
        color:grey;
        overflow: hidden;
        padding: 1.5rem .15rem;
        background-size: cover;
        background-position: center;
        background-color: #f9f9fd;
        text-align:center;
        margin: 0 -1rem;
    }}

    .hero_number_text{{    
        font-size:1.7em;
        color:#6c757d;
        font-weight:bold!important;
        margin:0;
    }}

    .small_header_text{{
        font-size:1em;
        color: #98a6ad!important;
        margin: auto;
        font-weight:400;
    }}
    
    .text_bold{{
        font-weight:bold;
    }}
        
    .accuracy_stats_container{{   
        height:320px;
    }}


    .flex-child_1 {{
        display:flex;
        flex-direction:column;
        align-items:center;
        margin:10px 0;
    }}

    .flex-parent{{
        display:flex;
        margin:2% 0;
        flex-direction:column;
        align-items:center;
        align-content:center;
        justify-content:center;
        flex-wrap:nowrap;
    }}

    .row_two_data_flx{{
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        align-items: center;
        justify-content:center;
        width:auto;
    }}
    
    .first_col_txt{{
        margin-left:10px;
        margin-right:10px;
    }}

    .second_col_txt{{
        margin-left:10px;
        margin-right:10px;
    }}
    
    .third_col_txt{{
        margin:0px
    }} 

    .margin_drop{{
        margin:0px
    }}
    
    .margin_3pc{{
        margin:2% 0;
    }}

    </style>
    """
    return ret


def data_widget_1_col(h1, stat1, h2, stat2):
    ret = f"""
    <div class="accuracy_stats_container data_widget">
      <div class="row h-100 flex-column">
        <div class="small_header_text">
            {h1}
            <div class="hero_number_text">{stat1}</div>
        </div>
        <div class="small_header_text">
            {h2}
            <div class="hero_number_text">{stat2}</div>
        </div> 
      </div>
    </div>
    """
    return ret


def data_widget_5_col(h1, stat1,
                      h2, stat2,
                      h3, stat3,
                      h4, stat4,
                      h5, stat5):
    ret = f"""
    <div class="player_stats_container data_widget">
      <div class="row h-100 flex-row">
        <div class="col-sm small_header_text">
            {h1}
            <div class="hero_number_text">{stat1}</div>
        </div>
        <div class="col-sm small_header_text">
            {h2}
            <div class="hero_number_text">{stat2}</div>
        </div> 
        <div class="col-sm small_header_text">
            {h3}
            <div class="hero_number_text">{stat3}</div>
        </div>
        <div class="col-sm small_header_text">
            {h4}
            <div class="hero_number_text">{stat4}</div>
        </div> 
        <div class="col-sm small_header_text">
            {h5}
            <div class="hero_number_text">{stat5}</div>
        </div>
      </div>
    </div>

    <style>    
    .player_stats_container {{
        margin:1rem 0px;

    }}
    </style>
    """
    return ret


def data_widget_2_col(h1, h2, stat1, stat2, stat3, stat4):
    ret = f"""
    <div class="accuracy_stats_container data_widget">
      <div class="row h-100 flex-parent">
        <div class="flex-child_1 small_header_text text_bold">
            Average accuracy
            <div class="row_two_data_flx">
                <div class="first_col_txt">
                    <div class="small_header_text">{h1}</div>
                    <div class="hero_number_text">{stat1}</div>
                </div>
                <div class="second_col_txt">    
                    <div class="small_header_text">{h2}</div>
                    <div class="hero_number_text">{stat2}</div>
                </div>
            </div>
        </div>
        <div class="flex-child_1 small_header_text text_bold">
            Highest accuracy
            <div class="row_two_data_flx">
                <div class="first_col_txt">
                    <div class="small_header_text">{h1}</div>
                    <div class="hero_number_text">{stat3}</div>
                </div>
                <div class="second_col_txt">    
                    <div class="small_header_text">{h2}</div>
                    <div class="hero_number_text">{stat4}</div>
                </div>
            </div>
        </div>       
      </div>
    </div>
    """
    return ret


def data_widget_3_col(h1, h2, h3, stat1, stat2, stat3, stat4, stat5, stat6):
    ret = f"""
    <div class="accuracy_stats_container data_widget margin_3pc">
      <div class="row h-100 flex-parent">
        <div class="flex-child_1 small_header_text text_bold margin_drop">
            Average accuracy
            <div class="row_two_data_flx">
                <div class="first_col_txt">
                    <div class="small_header_text">{h1}</div>
                    <div class="hero_number_text">{stat1}</div>
                </div>
                <div class="second_col_txt">    
                    <div class="small_header_text">{h2}</div>
                    <div class="hero_number_text">{stat2}</div>
                </div>
                <div class="third_col_txt">    
                    <div class="small_header_text">{h3}</div>
                    <div class="hero_number_text">{stat3}</div>
                </div>
            </div>
        </div>
        <div class="flex-child_1 small_header_text text_bold margin_drop">
            Highest accuracy
            <div class="row_two_data_flx">
                <div class="first_col_txt">
                    <div class="small_header_text">{h1}</div>
                    <div class="hero_number_text">{stat4}</div>
                </div>
                <div class="second_col_txt">    
                    <div class="small_header_text">{h2}</div>
                    <div class="hero_number_text">{stat5}</div>
                </div>
                <div class="third_col_txt">    
                    <div class="small_header_text">{h3}</div>
                    <div class="hero_number_text">{stat6}</div>
                </div>
            </div>
        </div>       
      </div>
    </div>
    """
    return ret

