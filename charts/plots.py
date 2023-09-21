# Glory Be The Lord

# Import libraries
import pandas as pd
import altair as alt
import streamlit as st


def bar_chart(data: pd.DataFrame, x: str):
    group = data.groupby([x])[x].count()
    data = pd.DataFrame({"count": group.values, x: group.index.astype(str)})

    bar = alt.Chart(data,
                    title=alt.TitleParams(
                        "Value Count Of %s" % x,
                        fontSize=20
                    )
                    ).mark_bar().encode(
        x=x,
        y="count",
        color=x
    ).properties(width=600)

    st.altair_chart(bar)


def highlighted_bar(data, x, y, highlight_type):
    bar = alt.Chart(data).mark_bar().encode(
        x=x,
        y=y,
        # The highlight will be set on the result of a conditional statement
        color=alt.condition(
            alt.datum[x] == (
                max(data[x]) if highlight_type == "max"
                else min(data[x])
            ),
            alt.value('orange'),
            alt.value('skyblue')
        )
    ).properties(width=600)

    print(alt.datum)

    st.altair_chart(bar)
