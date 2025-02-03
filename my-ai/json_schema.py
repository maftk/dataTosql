from pydantic import BaseModel
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["gemini_api_key"])


class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int


response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Give me information for the United States.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=CountryInfo,
    ),
)
print(response.text)
