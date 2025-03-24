import uuid 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from src.core.utils import setup_logger

logger = setup_logger(__file__)

def generate_vacation_idea_chain(
        month: int, 
        location: str, 
        days_rained: int, 
        days_cloudy: int, 
        days_sunny: int,
        crowded: str,
        activity: str,
        activities: list[str],

): 
    logger.info(f"Idea generation starting!")

    chat = ChatGoogleGenerativeAI()

    system_template = f"""
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
                    """
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = f"""
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

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    request = chat_prompt.format_prompt(
        month=month,
        location=location,
        days_rained=days_rained,
        days_cloudy=days_cloudy,
        crowded=crowded,
        activity=activity
    ).to_messages()

    result = chat(request)
    
    logger.info(f"Completed idea generation!")

    return result.content