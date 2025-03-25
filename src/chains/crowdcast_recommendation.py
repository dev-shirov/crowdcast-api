from src.core.utils import setup_logger

from google import genai

import os

from typing import Dict

from src.models.models import PredictionsModel

import pandas as pd

logger = setup_logger(__file__)


def generate_vacation_idea_chain(
    month: int,
    location: str,
    days_rained: int,
    days_cloudy: int,
    days_sunny: int,
    crowded: str,
    activity: str,
    api_response: Dict[str, list[PredictionsModel]],
):
    logger.info("Idea generation starting!")

    predictions = api_response["predictions"]

    predictions_list = [prediction.__dict__ for prediction in predictions]
    dataset = pd.DataFrame.from_records(predictions_list)[
        [
            "location",
            "month",
            "days_rained",
            "days_cloudy",
            "days_sunny",
            "tourists",
            "crowded",
            "water_sports_score",
            "hiking_score",
            "staycation_score",
            "nightlife_score",
        ]
    ].to_dict(orient="records")

    logger.info(f"{dataset}")

    prompt = f"""
                    You are a travel planner. Your goal is to recommend whether or not
                    a person should go to {location} on a specific month.

                    Take note of the following conditions:
                    1. Here is the dataset containing weather conditions and recommendations per activity for 
                    different months and locations: {dataset} Use this dataset only to make recommendations. 
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
                    - Days Rained: {days_rained}
                    - Days Cloudy: {days_cloudy}
                    - Days Sunny: {days_sunny}
                    - Tourist Crowds: {crowded}

                    Should I go to {location} on that month? Do not recommend crowded months.

                    Please follow this template with the following conditions:
                    1. If you recommend the user input activity, offer additional 
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

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents=prompt,
    )
    logger.info("Completed idea generation!")

    return response.text
