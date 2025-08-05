import os
import json
import openai
import pandas as pd
from helper_functions import llm

# Load the CSV file instead of JSON
csv_path = './data/courses.csv'
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()
df = df.fillna('')

# Function to check if the input text is appropriate
def check_moderation(text):
    response = llm.client.moderations.create(input=text)  # assuming llm.client is your OpenAI client
    result = response.results[0]
    return result.flagged, result.categories

# Build a dictionary: course title -> course details as dict
dict_of_courses = {
    row['Course Title'].strip(): row.to_dict()
    for _, row in df.iterrows()
}

# Build mapping: Competency -> list of course names
competency_n_course_name = {}
for _, row in df.iterrows():
    competency = row['Competency'].strip()
    course_name = row['Course Title'].strip()
    if competency not in competency_n_course_name:
        competency_n_course_name[competency] = []
    competency_n_course_name[competency].append(course_name)

def format_course_details(course_list):
    """Format list of course dicts into a readable string with all columns."""
    formatted_courses = []
    for idx, c in enumerate(course_list, start=1):
        details = [f"Course #{idx}:"]
        for k, v in c.items():
            v_str = v if v else "N/A"
            details.append(f"{k}: {v_str}")
        formatted_courses.append("\n".join(details))
    return "\n\n---\n\n".join(formatted_courses)

def identify_competency_and_courses(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with customer queries enclosed in {delimiter}.

    Decide if the query relates to any specific courses from this dictionary:
    {competency_n_course_name}

    Decide if the query is relevant to any specific courses
    in the Python dictionary below, where each key is a `competency`
    and the value is a list of `course_name`.

    If there are any relevant course(s), output a list of dictionary objects with:
    1) competency
    2) course_name

   If the query is generic or does not mention specific competencies,
   output a JSON list containing one object per competency,
   each with the competency name and one or two sample course names,
   to provide general recommendations.

   If no courses or competencies match, output an empty list.

    Ensure your response contains only the list of dictionary objects or an empty list, \
    without any enclosing tags or delimiters.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_message}{delimiter}"}
    ]

    response_str = llm.get_completion_by_messages(messages)
    response_str = response_str.replace("'", "\"")
    return json.loads(response_str)

def get_course_details(list_of_relevant_competency_n_course: list[dict]):
    course_names_list = [x.get('course_name') for x in list_of_relevant_competency_n_course]
    return [dict_of_courses.get(name) for name in course_names_list if name in dict_of_courses]


def generate_response_based_on_course_details(chat_history, user_message, product_details):
    delimiter = "####"
    
    system_message = f"""
    You are a helpful course assistant with the following course data:
    {product_details}

    User questions may ask about any course detail, including:
    - Course Title
    - Competency
    - Proficiency Level
    - Learning Outcomes
    - Training Period
    - Cost
    - Training Mode
    - Start and End Dates
    - Course Provider

    Answer ONLY using the data above. If a detail is missing, say so politely.
    
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about course(s), identify the relevant course(s) from the following list:
    {product_details}

    Step 2:{delimiter} Use the course information to answer the query. Only use facts from the product details provided. Be informative and detailed.

    Step 3:{delimiter} Answer the customer in a friendly and professional tone. Include pricing, delivery mode, duration, learning outcomes, and start/end dates. Use natural, clear language that aids decision-making.

    The conversation history is:
    {chat_history}

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>

    Include {delimiter} between steps.
    """

    # Prepare messages with prior chat included
    messages = [
        {'role': 'system', 'content': system_message},
    ]

    # Add prior chat messages as context (convert history dicts to string or similar)
    for msg in chat_history:
        messages.append({'role': msg['role'], 'content': msg['content']})

    # Add current user message
    messages.append({'role': 'user', 'content': f"{delimiter}{user_message}{delimiter}"})

    response_to_customer = llm.get_completion_by_messages(messages)
    return response_to_customer.split(delimiter)[-1]

def process_user_message(message_history, user_input):

  # Step 0: Check moderation on user input
    flagged, categories = check_moderation(user_input)
    if flagged:
        flagged_reasons = ', '.join([k for k, v in dict(categories).items() if v])
        warning_msg = f"⚠️ Your input was flagged for: {flagged_reasons}. Please revise your query."
        return warning_msg, []
    
    # Step 1: Identify courses based on user input (your original logic)
    competency_n_course_name = identify_competency_and_courses(user_input)
    print("Matched courses: ", competency_n_course_name)  # For debugging; remove or comment out to avoid double print

    # Step 2: Get course details for matched courses
    course_details = get_course_details(competency_n_course_name)

    # Step 3: Generate a detailed, friendly reply using course details and user input
    reply = generate_response_based_on_course_details(message_history, user_input, course_details)

    # Step 4: Check moderation on the generated reply too (recommended)
    flagged_resp, categories_resp = check_moderation(reply)
    if flagged_resp:
        reply = "⚠️ The generated response was flagged as potentially unsafe. Please try rephrasing your query."

    # Return the reply and updated conversation history
    return reply, course_details