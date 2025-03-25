# Import necessities 
import streamlit as st
from google import genai
import pandas as pd
import json

# Load CSV dataset
user_root = "/Users/xanvelaa/Desktop/"

# Load dataset
def load_data():
    data = pd.read_csv(user_root + "llm_dataset_updated.csv")  
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
a person should go to {location} on a specific month.

Take note of the following conditions:
1. Here is the dataset containing weather conditions and recommendations per activity for 
different months and locations: {df_dict} Use this dataset only to make recommendations. 
Do not make any recommendations based on information outside this dataset.

Take note that "True" means that a month is crowded and "False" means that a month is not crowded.

2. Do not recommend crowded months. If there is a high crowd, 
assume that a user would not want to go on that month anymore. All activities should not be recommended. 

3. If the month is too crowded, recommend a month that isn't crowded for the user to go to in order to 
enjoy their selected activity based on the user-input location. Check the dataset before recommending. 
Do not recommend a month if it's crowded. 

4. If you recommend another month for the activity, ensure that the recommendation 
does not contradict prior recommendations.

The user wants to go {activity} in {location} during the month of {month}. Based on:
- Days Rained: {selected_data['days_rained']}
- Days Cloudy: {selected_data['days_cloudy']}
- Days Sunny: {selected_data['days_sunny']}
- Tourist Crowds: {"High" if selected_data['crowded'] else "Low"}

Should I go to {location} on that month? Do not recommend crowded months.

Please follow this template with the following conditions:
1. If your recommend the user input activity, offer additional 
activities for Activity 2 and 3 and do not include activities 
that you don't recommend. 
2. If you do not recommend the user input activity, offer alternative activities.


Please make sure that the activities recommended are from this list only: 
["Water Sports", "Hiking", "Staycation", "Nightlife"].
Please note that the definition of "staycation" 
here is mostly focused on indoor activities (examples: pool, gym, spa)

For the first part, no need to explain.:
"Recommended or Not Recommended" {activity} \n
"Recommended or Not Recommended" Activity 2 \n
"Recommended or Not Recommended" Activity 3

Recommendation: 
Explain briefly. You can talk about the crowds and the weather.

"""

client = genai.Client(api_key= "put_api_key_here")
if st.button("Get Recommendation"):
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents = prompt)
    st.write(response.text)