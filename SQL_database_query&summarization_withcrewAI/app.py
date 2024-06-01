import sqlite3
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from crewai import Agent, Task, Crew, Process
import csv


load_dotenv()

# Retrieve the secrets
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Using Gemini Pro as LLM
llm = ChatGoogleGenerativeAI(
    model='gemini-pro', verbose=True, temperature=0.9, google_api_key=GOOGLE_API_KEY
)

@tool
def query_database(query: str,file_name):
    """Execute SQL query and return the result"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]  # Get column names
    conn.close()
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write the column headers
        writer.writerows(results) 
    return results


# Creating the Database Agent
db_query_agent = Agent(
    role="Database Query Agent",
    goal="You are a database query master. Your task is to convert the human question to an accurate SQL query, use the agent to query the database,save it to csv file and summarize the output.",
    backstory="You are a database query expert.",
    verbose=True,
    allow_delegation=False,

    
    llm=llm,
    tools=[query_database]
)

if __name__ == "__main__":
    user_query = "get me the names of top 3 highest earning persons from the employee table"
    csv_file = "results.csv"

    # Creating the task
    query = Task(
        description=f"Execute the {user_query} and save the output in {csv_file}, and summarise the queried output for human to understand",
        agent=db_query_agent,
        expected_output="Query the database, save it in a CSV file, and summarize the output in human readbale text."
    )

    crew = Crew(
        agents=[db_query_agent],
        tasks=[query],
        verbose=True,
        process=Process.sequential
    )

    crew.kickoff()
