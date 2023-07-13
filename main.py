import streamlit as st
import pandas as pd
import numpy as np
import json
import dateutil
import plost



## Utility Functions

def load_json(path:str) -> dict:
    with open(path) as f:
        data = json.load(f)
    return data

def pre_process(data_path, UTC_offset):    
    # load data
    songsDic = load_json(data_path)
    
    
    # Need to add unix time, currently api does this
    for song in songsDic["Items"]:
        t = dateutil.parser.parse(song["played_at"])
        song["unix_time"] = t.timestamp()
        song["played_at"] = t.strftime("%c")
    
    
    
    # Create df
    df = pd.DataFrame.from_dict(songsDic["Items"])

    # Add time information
    df['time'] = pd.to_datetime(df['unix_time'], unit="s") + pd.DateOffset(hours=UTC_offset)
    df['month'] = df['time'].dt.month
    df['weekday'] = df['time'].dt.dayofweek
    df['day_of_year'] = df['time'].dt.dayofyear
    df.set_index('time', inplace=True)
    df['hour_of_day'] = df.index.hour

    df["artist"] = [s.split("-")[-1].strip() for s in df.name]
    # need to sort so pandas doesnt break 
    df.sort_values(by="time",ascending=True, inplace=True)
    
    return df

# Main App

st.title('Test')

st.text('Spam one, spam two, spam there')

df = pre_process('songs.json', 10)


## Artists

artist_n = st.slider('Number of artist', 0, 130, 5)
artist_counts = df.artist.value_counts().head(n=artist_n).reset_index()

plost.pie_chart(
    data=artist_counts,
    title=f'Top {artist_n} Artists',
    theta='count',
    color='artist')


## Songs

song_n = st.slider('Number of Songs', 0, 130, 5)
song_counts = df.name.value_counts().head(n=song_n).reset_index()

plost.pie_chart(
    data=song_counts,
    title=f'Top {song_n} Songs',
    theta='count',
    color='name')

st.text('all')

st.table(df.head())