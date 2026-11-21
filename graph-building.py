# put streamlit code here as needed
import streamlit as st
import altair as alt
import pandas as pd


st.title("Streamlit App for Buildings Graphs")
st.text("These graphs are meant to show the statistics of each agency"
        "across the counties with the first graph showing how many are in each county"
        " and the second counting how many rennovations were made to each agency ")
st.text("Shows 2 data sets that take the count"
        " of the amount of zipcodes within each city "
        "and look at the agencies connected to them and see if "
        "they have been renovated over time")

df = pd.read_csv("https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv",
            na_values = {
                'Square Footage':0,
                'Year Acquired':0,
                'Year Constructed':0,
                'Total Floors':0
                })

df_group = df.groupby('City')['Zip code'].describe()
df_city = df_group[['count', 'max', 'min']]

df1_melt = df_city.reset_index().melt('City',
                                      var_name='City Stats',
                                      value_name='Stats')
chart1 = alt.Chart(df_city.reset_index()).mark_line(point=True).encode(
    alt.X('City:O'),
    alt.Y('count:Q', title='Count of zipcodes'),
    tooltip=['count']

).interactive()

chart1


df_groupBy2 = df.groupby('Agency Name')['Total Floors'].describe()


df_groupBy2 = df_groupBy2[['min','max']]

df2_melt  =  df_groupBy2.reset_index().melt('Agency Name',
                                           var_name = 'Statistic',
                                           value_name = 'Stats')


dropdown = alt.binding_select(options = ['max','min'], name = 'Floor Stat')

selection = alt.selection_point(fields = ['Statistic'], bind = dropdown, value = 'max')

color = alt.condition(selection,alt.Color('Statistic:N'), alt.value('lightgray'))



chart2 = alt.Chart(df2_melt.reset_index()).mark_area(point = True).encode(
        alt.X('Agency Name'),
        alt.Y('Stats:Q', scale=alt.Scale(type ='symlog'), title = 'Floors'),
        color = color,
        tooltip = ['Agency Name','Statistic','Stats' ]).add_params(
                selection)

chart2


tab1, tab2 = st.tabs(["Zipcode Building Count", "Floor Agency Changes"])

with tab1:
    st.altair_chart(chart1, theme="streamlit", use_container_width=True)
    st.text("This visualization displays the distribution of ZIP code statistics "
            "across different counties. I used a line graph to determine the points on the graph which "
            "show the count of how many zip codes in each city. For the encodings, I used a nominal type for City because it "
            "represents different city categories, a quantitative type for Stats because it contains numerical "
            "values and is supposed to count the number of zip codes. I also included tooltips that allow users to "
            "hover over individual points to see the count and made the graph interactive so the view can zoom "
            "in and out of the graph. These transformations helped summarize the ZIP code information and make comparisons between cities easier.")
    
with tab2:
    st.altair_chart(chart2, theme="streamlit", use_container_width=True)
    st.text("This visualization is mean to show the relationship between "
            "the total amount of floors with each agency. The graph is meant "
            "to show the changes brought to the mutiple agencies listed in the building over the years."
            " I used Altair to make an area graph to make it easier to show the difference "
            "between the minimum and maximum amounf of floors with each agency. "
            "I used Agency Name on the x-axis to identify each agency and Stats on the "
            "y-axis to represent the number of floors. For the encodings, I used a nominal"
            " type for Agency Name because the agencies are categories, a quantitative type "
            "for Stats because the number of floors is numerical, and a nominal type for Statistic"
            " to distinguish between the minimum and maximum values. I chose a symmetric "
            "logarithmic scale, 'symLog', for the y-axis to make differences between values "
            "easier to examine, especially when there are large variations in the number of floors. "
            "For interactivity, I added a dropdown menu that allows users to select either maximum or minimum."
            " The selected statistic is highlighted while the other appears in light gray, making it "
            "easier to compare the floor counts across different agencies.")
    
    
    