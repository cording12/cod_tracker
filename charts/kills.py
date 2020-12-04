import altair as alt


# # Configures the area portion of the chart

# # Figures out whether to use EKIAKDR or KDR for titles
# if kd_ratio == "kd":
#     kd_ratio_title = "KD Ratio"
# elif kd_ratio == "ekiadratio":
#     kd_ratio_title = "EKIA Ratio"
#
# # Configures the line portion of the chart
# # kd_line = base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
# kd_line = alt.Chart(final_data_frame).mark_line(interpolate="monotone").encode(
#     alt.X("match_number:Q"),
#     alt.Y(kd_ratio, title=kd_ratio_title),
# ).interactive()
#
# area_plot = alt.layer(kills_area, kd_line).resolve_scale(
#     y="independent").interactive()
#
# # Plots the data as a chart
# st.altair_chart(area_plot, use_container_width=True)
#
# # Test linear regression plot
#
# kd_points = alt.Chart(final_data_frame).mark_point().encode(
#     x="match_number",
#     y="deaths",
# )
#
# kd_reg_line = kd_points.transform_loess("match_number", "deaths").mark_line()
#
# # kd_reg = kd_points + kd_points.transform_regression("match_number", kd_ratio).mark_line()
# lyr = alt.layer(kd_points, kd_reg_line)


def kills_compare_chart(
        comp_mw, comp_bo4,
        final_data_frame,
        kills_type, kd_ratio):

    if kills_type == "EKIA":
        kills_type_title = "EKIA"
        kd_ratio_title = "EKIA Ratio"
    else:
        kills_type_title = "Kills"
        kd_ratio_title = "KD Ratio"

    if comp_mw or comp_bo4:
        # Draws the accuracy chart comparing Games
        selector = alt.selection_multi(
            fields=["Game"],
            bind="legend"
        )

        kills_area = alt.Chart(final_data_frame).mark_area().transform_fold(
            fold=["Game"],
        ).encode(
            alt.X("match_number", title="Match number"),
            alt.Y(kills_type, title=kills_type_title),
            color="Game",
            order=alt.Order("Game", sort="descending"),
            tooltip=[alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2")
                     ],
            opacity=alt.condition(selector, alt.value(0.85), alt.value(0.15))
        ).add_selection(
            selector
        ).interactive()

        chart_object = kills_area

    else:
        # Draws the accuracy chart without comparing games
        kills_area = alt.Chart(final_data_frame).mark_area(opacity=0.3).encode(
            alt.X("match_number", title="Match number"),
            alt.Y(kills_type, title="Kills type var here"),
            tooltip=[alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2"),
                     alt.Tooltip("match_number")
                     ]
        ).interactive()
        chart_object = kills_area

    return chart_object
