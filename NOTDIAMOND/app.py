#--NOTDIAMOND AND LLMROUTER--

##Installation
"""%pip install -qU langchain-openai
pip install --upgrade notdiamond"""

#LLM ROUTER
import os

os.environ["NOTDIAMOND_API_KEY"] = 'your_api_key'
os.environ["OPENAI_API_KEY"] = 'your_api_key'
os.environ["MISTRAL_API_KEY"] = "your_api_key"
os.environ["GOOGLE_API_KEY"] = 'your_api_key'

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
#########################################################################
#case1

chain = (
    PromptTemplate.from_template(
        """Given the user mathematical problem ,  classify them either addition or subtraction or multiplication or other category.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    | ChatOpenAI(model="gpt-4o")
    | StrOutputParser()
)

chain.invoke({"question": "add 3 and 4"})

##ans: Addition
################################################################################
#case2

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

chain = (
    PromptTemplate.from_template(
        """Given the user mathematical problem ,  classify them either addition or subtraction or multiplication or other category.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:"""
    )
    | ChatOpenAI(model="gpt-4o")
    | StrOutputParser()
)

chain.invoke({"question": "4-9"})
##ans: subtraction
##################################################################################



##NOTDIAMOND

from notdiamond import NotDiamond

client = NotDiamond()

llm_providers = [
    'openai/gpt-3.5-turbo-0125',
    'google/gemini-1.5-pro-latest'
]

#############
#case1
result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "give me python code for 2 sum problem."}  # Adjust as desired
    ],
  	model=llm_providers
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM output: 
 ```python
def two_sum(nums, target):
  """
  Finds two numbers in a list that add up to a target sum.

  Args:
    nums: A list of integers.
    target: The target sum.

  Returns:
    A list of two indices of the numbers that add up to the target sum,
    or None if no such pair is found.
  """
  seen = {}
  for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
      return [seen[complement], i]
    seen[num] = i
  return None

# Example usage
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(result)  # Output: [0, 1]
```

**Explanation:**

1. **Function Definition:**
   - The code defines a function `two_sum(nums, target)` that takes a list of integers (`nums`) and the target sum (`target`) as input.

2. **Hash Table (Dictionary):**
   - It initializes an empty dictionary called `seen` to store elements encountered in the list and their indices.

3. **Iterating through the List:**
   - The code iterates through the `nums` list using `enumerate` to get both the index (`i`) and the value (`num`) of each element.

4. **Calculating Complement:**
   - For each `num`, it calculates the `complement` needed to reach the `target` (`complement = target - num`).

5. **Checking for Complement:**
   - It checks if the `complement` is already present as a key in the `seen` dictionary:
     - If **yes**, it means the pair that sums to the target has been found. The function returns a list containing the index of the `complement` (stored in `seen[complement]`) and the current index `i`.
     - If **no**, the current `num` and its index `i` are added to the `seen` dictionary for future checks.

6. **Handling No Solution:**
   - If the loop completes without finding a pair, the function returns `None` indicating no solution exists.

**Example Usage:**

- In the example, `nums = [2, 7, 11, 15]` and `target = 9`.
- The code finds that `nums[0] + nums[1] = 2 + 7 = 9`.
- Therefore, the function returns `[0, 1]`, representing the indices of the solution pair."""

#####################
case2

result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the temperature at New Delhi?"}  # Adjust as desired
    ],
  	model=llm_providers
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM called: 
 gemini-1.5-pro-latest

LLM output: 
 I do not have access to real-time information, including weather data. To get the current temperature in New Delhi, I recommend checking a reliable weather website or app. """"

###############
case3

result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is the first president of USA"}  # Adjust as desired
    ],
  	model=llm_providers
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM called: 
 gemini-1.5-pro-latest

LLM output: 
 The first president of the United States of America was **George Washington**. """

##############
case4


#WITH and WITHOUT TRADEOFF
#1
result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the Gullivers' story in 30 words"}
    ],
  	model=llm_providers,
  	tradeoff="cost"
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM called: 
 gpt-3.5-turbo-0125

LLM output: 
 "Gulliver embarks on four journeys, encountering strange lands and creatures. He faces giants, tiny people, intellectuals, and talking horses, reflecting on society and human nature.""""

#2
result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the Gullivers' story in 30 words"}
    ],
  	model=llm_providers
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM called: 
 gemini-1.5-pro-latest

LLM output: 
 Shipwrecked surgeon Lemuel Gulliver encounters fantastical societies—tiny Lilliputians, giant Brobdingnagians, and more—on his voyages, satirizing humanity. """

###############
case5

#WITH and WITHOUT LATENCY
#1
result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the Gullivers' story in 80 words"}
    ],
  	model=llm_providers,
    tradeoff="latency"
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

"""
LLM called: 
 gpt-3.5-turbo-0125

LLM output: 
 "Gulliver's Travels" follows Lemuel Gulliver, a ship's surgeon, on his various adventures to different lands, each with its own unique inhabitants and customs. He encounters tiny people in Lilliput, giant beings in Brobdingnag, intelligent horses in Houyhnhnms, and irrational humans in the land of the Yahoos. Through his encounters, Gulliver reflects on the flaws of human nature and society, ultimately leading to his disillusionment with humanity and his desire to distance himself from it."""

#2

result, session_id, provider = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the Gullivers' story in 80 words"}
    ],
  	model=llm_providers
)

print("LLM called: \n", provider.model)
print("\nLLM output: \n", result.content)

LLM called: 
 gemini-1.5-pro-latest

"""
LLM output: 
 Shipwrecked surgeon Lemuel Gulliver finds himself on extraordinary adventures.  In Lilliput, he's a giant among tiny people. In Brobdingnag, he's a miniature marvel to giants. He encounters the flying island of Laputa, ruled by absent-minded intellectuals, and finally, the immortal but miserable Struldbrugs. Through his travels, Gulliver experiences the best and worst of humanity, leaving him forever changed. 
"""
