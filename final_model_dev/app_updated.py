# Import necessities 
import streamlit as st
from google import genai
import pandas as pd
import json

# Load CSV dataset
user_root = "/Users/xanvelaa/Desktop/"

# Load dataset
def load_data():
    data = pd.read_csv(user_root + "llm_dataset.csv")  
    data_json = data.to_dict(orient="records")
    return data, data_json

df, df_dict = load_data()

# Streamlit UI
st.title("🌴 Best Travel Time Recommender")

# User selects location, month, and activity
location = st.selectbox("Select a location:", df["location"].unique())
month = st.selectbox("Select a month:", df["month"].unique())
activity = st.selectbox("Select an activity:", ["Water Sports", "Hiking", "Staycation", "Nightlife"])

# Get selected month and location data
selected_data = df[(df["location"] == location) & (df["month"] == month)].iloc[0]

# Generate prompt for LLM
prompt = f"""
You are a travel planner. Your goal is to recommend whether or not
a person should go to {location} on a specific month. Take note that if
it's too crowded, the user might not want to go there. However, if it's
just rainy and not overcrowded, you can assume that a user wants to do other
activities from the list. If you don't recommend the first activity, recommend
another month for the user to go to in order to enjoy their selected 
activity. 

If you recommend another month for the activity, ensure that the recommendation 
does not contradict the conditions given for that month.

The user wants to go {activity} in {location} during the month of {month}. Based on:
- Days Rained: {selected_data['days_rained']}
- Days Cloudy: {selected_data['days_cloudy']}
- Days Sunny: {selected_data['days_sunny']}
- Tourist Crowds: {"High" if selected_data['crowded'] else "Low"}

Should I go to {location} on that month? 

Please follow this template.
If your recommend the user input activity, offer additional 
activities for Activity 2 and 3 and do not include activities 
that you don't recommend. If you do not recommend the user
input activity, offer alternative activities.

Please make sure that the activities recommended are from this list only: 
["Water Sports", "Hiking", "Staycation", "Nightlife"].
Please note that the definition of "staycation" 
here is mostly focused on indoor activities (examples: pool, gym, spa)

For the first part, no need to explain.:
"Recommended or Not Recommended" {activity} \n
"Recommended or Not Recommended" Activity 2 \n
"Recommended or Not Recommended" Activity 3

Recommendation: 
Explain briefly.

"""

client = genai.Client(api_key="put_api_key_here")
if st.button("Get Recommendation"):
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents = prompt)
    st.write(response.text)