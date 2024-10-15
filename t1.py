import fastf1 as ff1
import streamlit as st
import plotly.express as px
import pandas as pd

ff1.Cache.enable_cache('cache')

st.title("F1 Race and Qualifying Data Visualization")

Year = st.number_input("Enter the year of the race:", min_value=2018, max_value=2024, step=1)
Track = st.text_input("Enter the name of the track:")
stint = st.text_input("Enter 'R' for Race or 'Q' for Qualifying:")

if Year and Track and stint:
    session = ff1.get_session(Year, Track, stint)
    session.load()

    if stint == 'R':
        laps = session.laps
        st.subheader(f'Lap by Lap Positions for All Drivers at {Track} in {Year}', divider=True)
        fig = px.line(laps, x='LapNumber', y='Position', color='Driver')
        fig.update_layout(yaxis_title='Position', xaxis_title='Lap Number', yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)

        driver_positions = []
        results = session.results
        for index, row in results.iterrows():
            driver_number = row['DriverNumber']
            driver_info = session.get_driver(driver_number)
            driver_name = driver_info['BroadcastName']
            position = int(row['Position'])
            driver_positions.append({'Driver': driver_name, 'Position': position})

        df = pd.DataFrame(driver_positions)
        Winner = driver_positions[0]['Driver']
        st.subheader("RACE WINNER", divider=True)
        st.subheader(f'Winner of the race is {Winner}', divider=False)

        if Winner == "L HAMILTON":
            st.image("lewis.png")
        elif Winner == "M VERSTAPPEN":
            st.image("max.png")
        elif Winner == "C LECLERC":
            st.image("charles.png")

        st.subheader("FULL RESULTS", divider=True)
        st.table(df)

    elif stint == 'Q':
        fastest_laps = session.laps.pick_quicklaps()
        quali_results = fastest_laps[['Driver', 'LapTime', 'Compound', 'Sector1Time', 'Sector2Time', 'Sector3Time']].sort_values(by='LapTime').reset_index(drop=True)

        quali_results['Lap Time (s)'] = quali_results['LapTime'].dt.total_seconds()
        quali_results['Sector 1 (s)'] = quali_results['Sector1Time'].dt.total_seconds()
        quali_results['Sector 2 (s)'] = quali_results['Sector2Time'].dt.total_seconds()
        quali_results['Sector 3 (s)'] = quali_results['Sector3Time'].dt.total_seconds()

        st.write("Qualifying Results (in seconds):")
        st.dataframe(quali_results[['Driver', 'Lap Time (s)', 'Compound', 'Sector 1 (s)', 'Sector 2 (s)', 'Sector 3 (s)']])

        fig = px.bar(quali_results, x='Driver', y='Lap Time (s)', title=f"Qualifying Lap Times at {Track} in {Year}", labels={'y': 'Lap Time (s)'})
        st.plotly_chart(fig)

else:
    st.write("Please provide valid inputs for the year, track, and session type to display the graph.")
