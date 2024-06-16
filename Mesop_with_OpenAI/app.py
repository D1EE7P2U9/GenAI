import mesop as me
import mesop.labs as mel
import os
from mesop import stateclass
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage


llm = OpenAI(model="gpt-3.5-turbo", api_key="sk-") # paste your key


@stateclass
class State:
    pass

@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/",
    title="Mesop Chat with OpenAI",
)
def page():
    mel.chat(transform, title="Mesop Chat with OpenAI", bot_user="Mesop Bot")

def transform(input: str, history: list[mel.ChatMessage]):
    messages = [ChatMessage(role="system", content="You are a helpful assistant.")]
    messages.extend([ChatMessage(role="user", content=message.content) for message in history])
    messages.append(ChatMessage(role="user", content=input))

    resp = llm.stream_chat(messages)
    for r in resp:
        if r.delta:
            yield r.delta
