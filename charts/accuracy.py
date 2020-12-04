import altair as alt


def accuracy_compare_chart(
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

        # Area chart of accuracy
        acc_chart = alt.Chart(final_data_frame).mark_area().transform_fold(
            fold=["Game"],
        ).encode(
            alt.X("match_number", title="Match number"),
            alt.Y("accuracy", title="Accuracy"),
            color="Game",
            order=alt.Order("Game", sort="descending"),
            tooltip=[alt.Tooltip("Game"),
                     alt.Tooltip("accuracy", format="0.3", title="Accuracy"),
                     alt.Tooltip(kills_type, title=kills_type_title),
                     alt.Tooltip(kd_ratio, format="0.2", title=kd_ratio_title),
                     alt.Tooltip("map_name", title="Map name"),
                     alt.Tooltip("mode", title="Mode"),
                     alt.Tooltip("match_number", title="Match number")
                     ],
            opacity=alt.condition(selector, alt.value(0.85), alt.value(0.15))
        ).add_selection(
            selector
        ).interactive()

        chart_object = acc_chart

    else:
        # Draws the accuracy chart without comparing games
        acc_chart = alt.Chart(final_data_frame).mark_area(opacity=0.3).encode(
            alt.X("match_number", title="Match number"),
            alt.Y("accuracy:Q", title="Accuracy"),
            tooltip=[alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2"),
                     alt.Tooltip("match_number")
                     ]
        ).interactive()
        chart_object = acc_chart

    return chart_object

