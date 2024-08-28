from app import create_ical
import pandas as pd

schedule = pd.read_csv('schedule.csv')

schedule = schedule[schedule['Date'] != 'Date TBA']


# Clean up Opponent column formatting
schedule["Opponent"] = schedule["Opponent"].str.replace("@", "@ ").str.replace("vs", "vs. ").str.replace("*", "").str.strip()
schedule["Date"] = pd.to_datetime(schedule["Date"] + "/2024", format='%m/%d/%Y').dt.date

ids = [5241, 788, 2558, 2722, 2559, 2560, 5243, 
       8778, 7891, 5248, 8448, 5254]

filtered_schedule = schedule[schedule['id'].isin(ids)]

ical = create_ical(filtered_schedule)

# Convert iCal content to bytes
ical_content = ical.getvalue()

# Path to save the .ics file
ical_file_path = 'filtered_schedule.ics'

# Write the iCal content to a file
with open(ical_file_path, 'wb') as f:
    f.write(ical_content)