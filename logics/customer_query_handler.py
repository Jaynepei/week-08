import os
import json
import openai
import pandas as pd
from helper_functions import llm

# Load the CSV file instead of JSON
csv_path = './data/courses.csv'
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Fill NaNs with empty strings to avoid errors
df = df.fillna('')

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


def identify_competency_and_courses(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be enclosed in the pair of {delimiter}.

    Decide if the query is relevant to any specific courses
    in the Python dictionary below, where each key is a `competency`
    and the value is a list of `course_name`.

    If there are any relevant course(s), output a list of dictionary objects with:
    1) competency
    2) course_name

    {competency_n_course_name}

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
    #print("Raw LLM response:", response_str)  # DEBUG LINE
    response_str = response_str.replace("'", "\"")
    return json.loads(response_str)


def get_course_details(list_of_relevant_competency_n_course: list[dict]):
    course_names_list = [x.get('course_name') for x in list_of_relevant_competency_n_course]
    return [dict_of_courses.get(name) for name in course_names_list]


def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about course(s), \
    identify the relevant course(s) from the following list:
    {product_details}

    Step 2:{delimiter} Use the course information to answer the query. \
    Only use facts from the product details provided. Be informative and detailed.

    Step 3:{delimiter} Answer the customer in a friendly and professional tone. \
    Include pricing, delivery mode, duration, learning outcomes, and start/end dates. \
    Use natural, clear language that aids decision-making.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>

    Include {delimiter} between steps.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_message}{delimiter}"}
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    return response_to_customer.split(delimiter)[-1]


def process_user_message(user_input):
    # Step 1: Identify course categories
    competency_n_course_name = identify_competency_and_courses(user_input)
    print("Matched courses: ", competency_n_course_name)

    # Step 2: Get course details
    course_details = get_course_details(competency_n_course_name)

    # Step 3: Generate final customer-facing response
    reply = generate_response_based_on_course_details(user_input, course_details)
#     return reply, course_details

def process_user_message(message_history, user_input):
 # Append the new user message to history
    message_history.append({"role": "user", "content": user_input})

    # Step 1: Identify courses based on user input (your original logic)
    competency_n_course_name = identify_competency_and_courses(user_input)
    print("Matched courses: ", competency_n_course_name)  # For debugging; remove or comment out to avoid double print

    # Step 2: Get course details for matched courses
    course_details = get_course_details(competency_n_course_name)

    # Step 3: Generate a detailed, friendly reply using course details and user input
    reply = generate_response_based_on_course_details(user_input, course_details)

    # Append assistant reply to history
    message_history.append({"role": "assistant", "content": reply})

    # Return the reply and updated conversation history
    return reply, course_details