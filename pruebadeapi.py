import os
import openai
import streamlit as st

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

#openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = "sk-00PiTVd2CxO021kMskVT3BlbkFJ0ySNxq0zREInl3wD5r7b" # Generic API
openai.api_key = OPENAI_API_KEY

print(openai.api_key)
