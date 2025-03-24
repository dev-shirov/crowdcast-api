# Import necessities 
import streamlit as st
from google import genai
import pandas as pd
import json

# Load CSV dataset
user_root = "/Users/xanvelaa/Desktop/"

# Load dataset
def load_data():
    return pd.read_csv(user_root + "train_data_updated.csv")  

df = load_data()

# Compute crowded months per location
df["crowded"] = df.groupby("location")["tourists"].transform(lambda x: x > x.median())

# Define activity preferences
activity_preferences = {
    "Water Sports": {"days_sunny": 1, "days_cloudy": 0.5, "days_rained": -0.5},
    "Hiking": {"days_sunny": 1, "days_cloudy": 0.5, "days_rained": -0.3},  
    "Staycation": {"days_sunny": -0.5, "days_cloudy": 1, "days_rained": 2},
    "Nightlife": {"days_sunny": -0.5, "days_cloudy": 2, "days_rained": 1}
      
}

# Compute scores dynamically for all locations
for activity in activity_preferences:
    df[f"{activity}_score"] = df.apply(lambda row: sum(
        row[key] * weight for key, weight in activity_preferences[activity].items()
    ), axis=1)

print(df)

# # Streamlit UI
# st.title("🌴 Best Travel Time Recommender")

# # User selects location, month, and activity
# location = st.selectbox("Select a location:", df["location"].unique())
# month = st.selectbox("Select a month:", df["month"].unique())
# activity = st.selectbox("Select an activity:", list(activity_preferences.keys()))

# # Get selected month and location data
# selected_data = df[(df["location"] == location) & (df["month"] == month)].iloc[0]

# # Generate prompt for LLM
# prompt = f"""
# You are a travel planner. Your goal is to recommend whether or not
# a person should go to {location} on a specific month. Take note that if
# it's too crowded, the user might not want to go there. However, if it's
# just rainy and not overcrowded, you can assume that a user is still open
# to a staycation at a hotel or resort. If your answer is no, recommend
# another month for the user to go to in order to enjoy their selected 
# activity.

# The user wants to go {activity} in {location} during the month of {month}. Based on:
# - Days Rained: {selected_data['days_rained']}
# - Days Cloudy: {selected_data['days_cloudy']}
# - Days Sunny: {selected_data['days_sunny']}
# - Tourist Crowds: {"High" if selected_data['crowded'] else "Low"}

# Should I go to {location} on that month? Explain briefly.
# """

# client = genai.Client(api_key="AIzaSyCgO_05ibuYEdXgZBXt6dtFfQH6j7WSBJg")
# if st.button("Get Recommendation"):
#     response = client.models.generate_content(
#         model="gemini-1.5-pro",
#         contents = prompt)
#     st.write(response.text)
 