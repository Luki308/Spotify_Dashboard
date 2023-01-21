import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib

st.title("How much do we share listening to our favourite artists?")

df1 = pd.read_json('./Lukasz/long/endsong_0.json')
df2 = pd.read_json('./Agata/extended/endsong_0.json')
df3 = pd.read_json('./Karolina/endsong.json')

artist_chosen = st.selectbox("Choose an artist",
             ["Adele", "The Dumplings","Maanam", "Michael Jackson", "Daria Zawiałow"])

names = ["Łukasz", "Agata", "Karolina"]
colors = ["#1db954","#083318","#10642d"]
frames = [df1, df2, df3]
df_plot_year = None
df_plot_name = None
all_of_artist = 0
year_len = []
i = 0
for df in frames:
    # Filtering for chosen artist by year
    df_filter_by_artist = df.loc[
        df.master_metadata_album_artist_name == artist_chosen].reset_index(drop=True)
    df_filter_by_artist['Year'] = pd.to_datetime(df_filter_by_artist["ts"]).dt.strftime('%Y')
    df_filter_by_artist = df_filter_by_artist.groupby("Year").master_metadata_album_artist_name.agg(
        'count').reset_index() \
        .rename(columns={"master_metadata_album_artist_name": "count"})
    df_plot_year = pd.concat([df_plot_year, df_filter_by_artist])

    # Summing tracks
    suma = sum(df_filter_by_artist['count'])
    all_of_artist += suma

    # Prepering df with names
    df_plot_name = pd.concat([df_plot_name, pd.DataFrame({
        'Name': [names[i]],
        'count': [suma]
    })])
    i += 1

    year_len.append(len(df_filter_by_artist))

df_plot_year = df_plot_year.reset_index(drop=True)
min_year = int(df_plot_year['Year'].min())
max_year = int(df_plot_year['Year'].max())
years = list(range(min_year, max_year+1))

# Data for Sankey diagram
label = ['Sum of all tracks'] + df_plot_name['Name'].tolist() + years
source = []
target = []
value = []
color = []
for i in range(len(df_plot_name)):
    source += [0]
    target += [i + 1]
    color += [colors[i]]
    print(color)
value += df_plot_name['count'].tolist()

chosen_year = 0
for i in range(len(df_plot_name)):
    for j in range(year_len[i]):
        source += [1 + i]
        target += [label.index(int(df_plot_year.loc[chosen_year+j,'Year']))]
        color += [colors[i]]
        print(color)
    chosen_year += year_len[i]
value += df_plot_year['count'].tolist()

# node_x = [0]+[1]*len(df_plot_name)+[2]*len(df_plot_year)
# node_y = [0]+[_ for _ in range(len(df_plot_name))]+[_ for _ in range(len(df_plot_year))]
#
# print(node_x)
# print(node_y)

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=label,
        color = px.colors.qualitative.Light24
        # x = node_x,
        # y = node_y,

    ),
    link=dict(
        source = source,
        target = target,
        value = value,
        color = color
    )
)])
#color = "#1db954"
fig.update_layout(title_text=" Sankey plot for chosen artist ", font_size=18)

st.plotly_chart(fig)