import pandas as pd
import streamlit as st
import datetime
import icalendar
from io import BytesIO

# Load the schedule
schedule = pd.read_csv('schedule.csv')

# Filter out 'Date TBA' entries
schedule = schedule[schedule['Date'] != 'Date TBA']

# Clean up Opponent column formatting
schedule["Opponent"] = schedule["Opponent"].str.replace("@", "@ ").str.replace("vs", "vs. ").str.replace("*", "").str.strip()
schedule["Date"] = pd.to_datetime(schedule["Date"] + "/2024", format='%m/%d/%Y').dt.date

st.title('Georgia HS Fall 2024 Schedule')

# Team selection checkboxes
select_all = st.checkbox('Select All Teams', value=False)
select_all_default = st.checkbox('Select All Default Teams', value=False)

default_teams = ['Riverwood Raiders', 'Brookwood Broncos', 'Pierce County Bears', 'Mount Paran Christian Eagles', 
                 'Buford Wolves', 'East Coweta Indians', 'Cherokee Bluff Bears', 'East Forsyth Broncos', 
                 'West Forsyth Wolverines', 'Northside Eagles', 'Peach County Trojans']

all_teams = sorted(schedule['Team'].unique())

# Team selection
if select_all_default:
    teams = st.multiselect('Select Teams', all_teams, default=default_teams)
else:
    teams = st.multiselect('Select Teams', all_teams)

if select_all:
    teams = all_teams

# Filter schedule by selected teams and date range
filtered_schedule = schedule[schedule['Team'].isin(teams)]

start_date = st.date_input('Start Date', pd.to_datetime(datetime.datetime.now().date()))
end_date = st.date_input('End Date', pd.to_datetime('2024-12-31'))

filtered_schedule = filtered_schedule[(filtered_schedule['Date'] >= start_date) & (filtered_schedule['Date'] <= end_date)]
filtered_schedule = filtered_schedule[['Date', 'Time', 'Team', 'Opponent']].sort_values(by=['Date', 'Time'])

# Display the filtered schedule
st.dataframe(filtered_schedule, use_container_width=True)


# Function to create an iCal file
def create_ical(schedule_df):
    cal = icalendar.Calendar()
    for index, row in schedule_df.iterrows():
        event = icalendar.Event()
        event.add('summary', f"{row['Team']} vs. {row['Opponent']}")
        
        # Adjust parsing to handle time format '5:00pm'
        event_start_time = datetime.datetime.strptime(row['Time'].replace(" ", ""), "%I:%M%p").time()
        event_start = datetime.datetime.combine(row['Date'], event_start_time)
        event_end = event_start + datetime.timedelta(hours=2)  # Assuming a 2-hour game
        
        event.add('dtstart', event_start)
        event.add('dtend', event_end)
        event.add('dtstamp', datetime.datetime.now())
        cal.add_component(event)
    
    ical_bytes = BytesIO()
    ical_bytes.write(cal.to_ical())
    ical_bytes.seek(0)
    
    return ical_bytes

# Create the iCal file if there are games in the filtered schedule
if not filtered_schedule.empty:
    ical_file = create_ical(filtered_schedule)
    st.download_button(label='Download iCal', data=ical_file, file_name='game_schedule.ics', mime='text/calendar')
else:
    st.write("No games found for the selected criteria.")
