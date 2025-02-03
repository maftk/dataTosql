import asyncio
from google import genai
from google.genai import types
from pydantic import BaseModel
import os

client = genai.Client(api_key=os.environ["gemini_api_key"])

# Json Schema
class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int


def json_schema():
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Give me information for the United States.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CountryInfo,
        ),
    print(response.text)
    )

# List Models Static
def list_models():
    for model in client.models.list(config={'query_base':True}):
        print(model.name)


def pager_models():
    pager = client.models.list(config={"page_size": 10, 'query_base':True})

    print(pager.page_size)
    print(pager[0])
    pager.next_page()
    print(pager[0])

async def list_models_as():
    async for job in await client.aio.models.list(config={'query_base':True}):
        print(job)

# List Job
async def list_tune_jobs_async():
    async for job in await client.aio.tunings.list(config={"page_size": 10}):
        print(job)


# Stream Chat
def chat_stream():
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-exp", contents="Tell me a story in 300 words."
    ):
        print(chunk.text, end="")

async def chat_stream_as():
    chat = client.aio.chats.create(model="gemini-2.0-flash-exp")
    async for chunk in await chat.send_message_stream("tell me a story"):
        print(chunk.text, end="")

if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(list_tune_jobs_async())
