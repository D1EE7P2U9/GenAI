import boto3
import json
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
aws_region = os.getenv('region_name')
modelId = os.getenv('modelId')
agentAliasId = os.getenv('agentAliasId')
agentId = os.getenv('agentId')
sessionId = os.getenv('sessionId')

# creating bedrock client

bedrock = boto3.client("bedrock-runtime", 
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region)

st.title("AWS BEDROCK TEXT SUMMARIZATION")


sample_question = st.text_input("give me the text to summarize")

# content to summarized

# sample_question = """
# Startups move quickly, and engineering is often prioritized over documentation. Unfortunately, this prioritization 
# leads to release cycles that don’t match, where features release but documentation 
# lags behind. This leads to increased support calls and unhappy customers.
# Skyflow is a data privacy vault provider that makes it effortless to secure sensitive 
# data and enforce privacy policies. Skyflow experienced this growth and documentation challenge in 
# early 2023 as it expanded globally from 8 to 22 AWS Regions, including China and other areas of the world. 
# The documentation team, consisting of only two people, found itself overwhelmed as the engineering team, with 
# over 60 people, updated the product to support the scale and rapid feature release cycles.
# Given the critical nature of Skyflow’s role as a data privacy company, the stakes were particularly high. 
# Customers entrust Skyflow with their data and expect Skyflow to manage it both securely and accurately. 
# The accuracy of Skyflow’s technical content is paramount to earning and keeping customer trust. 
# Although new features were released every other week, documentation for the features took an average 
# of 3 weeks to complete, including drafting, review, and publication. The following diagram illustrates 
# their content creation workflow.
# """

prompt = "You are a content summarization expert, understand the given content , summarize it meaningfully without hallucination and should not miss any important information while summarizing."


final_prompt = "\n\nHuman:"+prompt + sample_question +"n\nAssistant:"


prompt = f"<s>[INST] {final_prompt} [/INST]"

native_request = {
    "prompt": prompt,
    "max_tokens": 512,
    "temperature": 0.5,
}

# Convert the native request to JSON.
request = json.dumps(native_request)

response = bedrock.invoke_model(modelId=modelId, body=request)

model_response = json.loads(response["body"].read())


output = model_response["outputs"][0]["text"]

st.write("Your Summary:", output)
