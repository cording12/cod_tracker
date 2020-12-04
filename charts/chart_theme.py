# Credit to Peter Baumgartner who published this paper
# https://pmbaumgartner.github.io/streamlitopedia/front/introduction.html
# which explains all the styling used

# Dark blue
colour1 = "071128"
colour1_hex = "#" + colour1

# Purple
colour2 = "737DF4"
colour2_hex = "#" + colour2

# Aqua
colour3 = "26ede8"
colour3_hex = "#" + colour3

# # Grey
# colour4 = "90A7B2"
# colour4_hex = "#" + colour4

# Green - neon
colour4 = "0ACF97"
colour4_hex = "#" + colour4

# Green - muted
colour5 = "007878"
colour5_hex = "#" + colour5

text_colour = "071128"
text_colour_hex = "#" + text_colour

text_colour_light = "adb5bd"  # 98a6ad
text_colour_light_hex = "#" + text_colour_light

text_colour_darker = "98a6ad"
text_colour_darker_hex = "#" + text_colour_darker


def colour_pallete_checker(col1, col2, col3, col4, col5):
    # This function to run a webpage that displays the colour
    col1r = col1
    col2r = col2
    col3r = col3
    col4r = col4
    col5r = col5
    view_url = f"https://coolors.co/{col1r}-{col2r}-{col3r}-{col4r}-{col5r}"
    return view_url


# print(colour_pallete_checker(colour1, colour2, colour3, colour4, colour5))


def streamlit_theme():
    font = "Nunito Sans, sans-serif"
    axis_font = "Nunito Sans, sans-serif"
    primary_colour = colour1_hex
    font_colour_dark = text_colour_hex
    font_colour_light = text_colour_light_hex
    font_colour_regular = text_colour_darker_hex
    font_weight_light = 400
    base_size = 14
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75

    config = {
        "config": {
            "arc": {"fill": colour2_hex},
            "area": {"fill": colour4_hex},
            "circle": {"fill": colour2_hex, "stroke": colour4_hex, "strokeWidth": 0.5},
            "line": {"stroke": colour2_hex},
            "path": {"stroke": colour2_hex},
            "point": {"stroke": colour2_hex},
            "rect": {"fill": colour2_hex},
            "shape": {"stroke": colour2_hex},
            "symbol": {"fill": colour2_hex},
            "title": {
                "font": font,
                "color": font_colour_dark,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_colour_regular,
                "titleFontSize": sm_font,
                "titleFontWeight": font_weight_light,
                "labelFont": axis_font,
                "labelColor": font_colour_light,
                "labelFontWeight": font_weight_light,
                "gridColor": "#FAFAFA",
                "domainColor": "#FAFAFA",
                "tickColor": "#FAFAFA",
            },
            "axisTop": {
                # Disables the top axis by setting font size to 0 and colours invisible
                "labelFontSize": 0,
                "domaincolor": "#fff",
                "tickcolor": "#fff",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titlecolor": font_colour_dark,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelcolor": font_colour_dark,
                "labelFontSize": sm_font,
                "orient": "top",
            },
            "view": {
                "height": 350
            },
            "range": {
                "category": [colour1_hex, colour2_hex, colour3_hex, colour4_hex, colour5_hex],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config

# def streamlit_theme_backup():
#     font = "Nunito,sans-serif"
#     axis_font = "Nunito,sans-serif"
#     primary_colour = colour1_hex
#     font_colour = text_colour_hex
#     light_font_colour = text_colour_light
#     grey_colour = "#F0F2F6"
#     base_size = 14
#     lg_font = base_size * 1.25
#     sm_font = base_size * 0.8  # st.table size
#     xl_font = base_size * 1.75
#
#     config = {
#         "config": {
#             "arc": {"fill": primary_colour},
#             "area": {"fill": colour4_hex},
#             "circle": {"fill": primary_colour, "stroke": font_colour, "strokeWidth": 0.5},
#             "line": {"stroke": primary_colour},
#             "path": {"stroke": primary_colour},
#             "point": {"stroke": primary_colour},
#             "rect": {"fill": primary_colour},
#             "shape": {"stroke": primary_colour},
#             "symbol": {"fill": primary_colour},
#             "title": {
#                 "font": font,
#                 "colour": font_colour,
#                 "fontSize": lg_font,
#                 "anchor": "start",
#             },
#             "axis": {
#                 "titleFont": axis_font,
#                 "titlecolour": font_colour,
#                 "titleFontSize": sm_font,
#                 "labelFont": font,
#                 "labelcolour": font_colour,
#                 "labelFontSize": sm_font,
#                 "gridcolour": grey_colour,
#                 "domaincolour": "#C1C1C1",
#                 "tickcolour": "#C1C1C1",
#             },
#             "axisTop": {
#                 # Disables the top axis by setting font size to 0 and colours invisible
#                 "labelFontSize": 0,
#                 "domaincolour": "#fff",
#                 "tickcolour": "#fff",
#             },
#             "header": {
#                 "labelFont": font,
#                 "titleFont": font,
#                 "labelFontSize": base_size,
#                 "titleFontSize": base_size,
#             },
#             "legend": {
#                 "titleFont": font,
#                 "titlecolour": font_colour,
#                 "titleFontSize": sm_font,
#                 "labelFont": font,
#                 "labelcolour": font_colour,
#                 "labelFontSize": sm_font,
#                 "orient": "top",
#             },
#             "view": {
#                 "height": 350
#             },
#             "range": {
#                 "category": [colour1_hex, colour2_hex, colour3_hex, colour4_hex, colour5_hex],
#                 "diverging": [
#                     "#850018",
#                     "#cd1549",
#                     "#f6618d",
#                     "#fbafc4",
#                     "#f5f5f5",
#                     "#93c5fe",
#                     "#5091e6",
#                     "#1d5ebd",
#                     "#002f84",
#                 ],
#                 "heatmap": [
#                     "#ffb5d4",
#                     "#ff97b8",
#                     "#ff7499",
#                     "#fc4c78",
#                     "#ec245f",
#                     "#d2004b",
#                     "#b10034",
#                     "#91001f",
#                     "#720008",
#                 ],
#                 "ramp": [
#                     "#ffb5d4",
#                     "#ff97b8",
#                     "#ff7499",
#                     "#fc4c78",
#                     "#ec245f",
#                     "#d2004b",
#                     "#b10034",
#                     "#91001f",
#                     "#720008",
#                 ],
#                 "ordinal": [
#                     "#ffb5d4",
#                     "#ff97b8",
#                     "#ff7499",
#                     "#fc4c78",
#                     "#ec245f",
#                     "#d2004b",
#                     "#b10034",
#                     "#91001f",
#                     "#720008",
#                 ],
#             },
#         }
#     }
#     return config
