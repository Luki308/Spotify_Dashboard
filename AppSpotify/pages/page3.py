import datetime
from datetime import date

import clr as clr
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.colors as clr
from matplotlib.colors import ListedColormap
from streamlit_extras.app_logo import add_logo

#st.set_page_config(layout="wide")

add_logo("./spotify.png", height=300)

page_bg_img = """
<style>
[data-testid="stSidebar"]{
    background-color: #1db954
}
</style>
"""

with st.sidebar:
    st.markdown(page_bg_img,unsafe_allow_html=True)


#col1, col2, col3 = st.columns([1,5,1])

#with col2:
st.title("When and what do we listen to most often?")
data = st.radio("Which data to display?", ["Agata", "Karolina","Łukasz"])

if data == "Agata":
    df = pd.read_json("./Agata/StreamingHistory0.json")
    df1 = pd.read_json("./Agata/StreamingHistory1.json")
    df = df.append(df1, ignore_index=True).query("msPlayed>30000")

if data == "Karolina":
    df = pd.read_json("./Agata/StreamingHistory0.json")
    df = df.query("msPlayed>30000")

if data == "Łukasz":
    df = pd.read_json("./Lukasz/short/StreamingHistory0.json")
    df1 = pd.read_json("./Lukasz/short/StreamingHistory1.json")
    df2 = pd.read_json("./Lukasz/short/StreamingHistory2.json")
    df = df.append(df1, ignore_index=True).append(df2, ignore_index=True).query("msPlayed>30000")

#df = pd.read_json("./" + data + "/StreamingHistory0.json")
#try:
#    df1 = pd.read_json("./" + data + "/StreamingHistory1.json")
#except FileNotFoundError as e:
#    df1 = []

#df = df.append(df1, ignore_index=True).query("msPlayed>30000")
df["endTime"] = pd.to_datetime(df["endTime"])
#df = df.loc[(df['endTime']>=start) & (df['endTime']<=end)]

#with col2:
start = st.date_input("Enter the start date",min_value=df["endTime"].min(),
                      max_value=df["endTime"].max(), value=df["endTime"].min())
end = st.date_input("Enter the end date",min_value=df["endTime"].min(),
                      max_value=df["endTime"].max(), value=df["endTime"].max())

df= df.loc[(df["endTime"].dt.date>start) &(df["endTime"].dt.date<end)]
df["weekday"] = df["endTime"].dt.day_name()
df["hour"] = df["endTime"].dt.hour
df["count"] = df.groupby(["hour", "weekday"])["weekday"].transform('count')
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekday'] = pd.Categorical(df['weekday'], categories=cats, ordered=True)
df = df.sort_values('weekday')

#df.info()

df1 = df[['hour', 'weekday', 'count']]
#print(df1.head())
#print(df1.info())
df2=pd.DataFrame({'hour': [i for i in range(0,24)],
                  'weekday': ["Monday" for i in range(0,24)],
                  'count':[0 for i in range(0,24)]})
df1 = df1.append(df2, ignore_index=True)

x = pd.DataFrame(df1['weekday'].unique())
heatmap_pt = pd.pivot_table(df1, values='count', index=['hour'], columns='weekday')
fig, ax = plt.subplots(figsize=(16, 8))
ax.set(ylim=(0, 24))
sns.set(rc={'axes.facecolor':"#0a0909", 'figure.facecolor':"#0a0909"})
mpl.rcParams.update({'text.color' : "white",
                     'axes.labelcolor' : "white",
                     #'legend.labelcolor': "white",
                     'legend.edgecolor':"white",
                     'legend.facecolor':"white",
                     'xtick.color':"white",
                     'ytick.color':"white"})

#gyr = ['#28B463','#FBFF00', '#C0392B']
#my_colors = ListedColormap(sns.color_palette(gyr))     201A1A      2CFF77
#cmap=sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)
my_colors = clr.LinearSegmentedColormap.from_list('custom blue', ['#0d0c0c','#0ABD4A','#A2FFC4'], N=256)
sns.heatmap(heatmap_pt, cmap=my_colors)
plt.xticks(rotation=15)




#st.write(a)
#with col2:
st.pyplot(fig)
