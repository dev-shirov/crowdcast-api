from src.core.utils import setup_logger

from google import genai

import os

from typing import Optional

logger = setup_logger(__file__)


def generate_vacation_idea_chain(
    month: int,
    location: str,
    days_rained: int,
    days_cloudy: int,
    days_sunny: int,
    crowded: str,
    activity: str,
    activities: Optional[str] = None,
):
    logger.info("Idea generation starting!")


    prompt = f"""
                        You are a travel planner. Your goal is to recommend whether or not
                        a person should go to {location} on a specific month. Take note that if
                        it's too crowded, the user might not want to go there. However, if it's
                        just rainy and not overcrowded, you can assume that a user to other
                        activities from the list. If your answer is no, recommend
                        another month for the user to go to in order to enjoy their selected 
                        activity.

                        The user wants to go {activity} in {location} during the month of {month}. Based on:
                        - Days Rained: {days_rained}
                        - Days Cloudy: {days_cloudy}
                        - Days Sunny: {days_sunny}
                        - Tourist Crowds: {"High" if crowded else "Low"}

                        Should I go to {location} on that month? 

                        Please follow this template. Please offer additional/alternative activities for Activity 2 and 3. Please
                        make sure that the activities recommended are from this list only: ["Water Sports", "Hiking", "Staycation", "Nightlife"]
                        For the first part, no need to explain.:
                        Check Mark/Wrong emoji {activity} \n
                        Check Mark/Wrong emoji Activity 2 \n
                        Check Mark/Wrong emoji Activity 3

                        Recommendation: 
                        Explain briefly.
                    """

    client = genai.Client(api_key="AIzaSyBjfVn2xPzNMTgIA_l-2_3l7h6b90a1X7Q" )

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents = prompt,
    )
    logger.info("Completed idea generation!")

    return response.text

