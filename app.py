import streamlit as st
from openai import OpenAI
import os
import json

# set the env var 

client = OpenAI()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Streamlit UI
st.title("SQL Query Generator")

# Input schema
schema = st.text_area("Enter schema:")

# Input question
question = st.text_input("Enter your question:")

# Function to generate SQL query
def generate_sql_query(schema, question):
    # Function to send text to ChatGPT API
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "Given the following schema, your job is to write an SQL query for the user’s question.\n" + schema
        },
        {
        "role": "user",
        "content": "Write a SQL query for the Question: " + question 
        }
    ],
    temperature=0.7,
    max_tokens=64,
    top_p=1
    )
    res = json.loads(response.json())
    if res:
        print("===================")
        print(res)
        print("===================")
        res = res['choices'][0]['message']['content']
        res = res.replace("```", "")
        res = res.replace("sql", "")
        return res
    else:
        return "Error: Failed to generate response."

# Button to trigger generation
if st.button("Generate SQL Query"):
    if schema.strip() != "" and question.strip() != "":
        # Generate SQL query
        sql_query = generate_sql_query(schema, question)
        # Display SQL query
        st.write("Generated SQL query:")
        st.code(sql_query, language="sql")
    else:
        st.warning("Please enter schema and question.")
