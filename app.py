import pandas as pd
import streamlit as st

schedule = pd.read_csv('schedule.csv')

schedule = schedule[schedule['Date'] != 'Date TBA']

schedule["Opponent"] = schedule["Opponent"].str.replace("@", "@ ").str.replace("vs", "vs. ").str.replace("*", "").str.strip()
schedule["Date"] = pd.to_datetime(schedule["Date"] + "/2024", format='%m/%d/%Y').dt.date

st.title('Georgia HS Fall 2024 Schedule')

default_teams = ['Riverwood Raiders', 'Brookwood Broncos', 'Pierce County Bears', 'Mount Paran Christian Eagles', 
                 'Buford Wolves', 'East Coweta Indians', 'Cherokee Bluff Bears', 'East Forsyth Broncos', 
                 'West Forsyth Wolverines', 'Northside Eagles']

all_teams = sorted(schedule['Team'].unique())

teams = st.multiselect('Select Teams', all_teams, default=default_teams)

select_all = st.checkbox('Select All Teams', value=False)

if select_all:
    teams = all_teams


filtered_schedule = schedule[schedule['Team'].isin(teams)]

start_date = st.date_input('Start Date', pd.to_datetime('2024-08-01'))
end_date = st.date_input('End Date', pd.to_datetime('2024-12-31'))

filtered_schedule = filtered_schedule[(filtered_schedule['Date'] >= start_date) & (filtered_schedule['Date'] <= end_date)]

filtered_schedule = filtered_schedule[['Date', 'Time', 'Team', 'Opponent']].sort_values(by=['Date', 'Time'])

st.dataframe(filtered_schedule, use_container_width=True)