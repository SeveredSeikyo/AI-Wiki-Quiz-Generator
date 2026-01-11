import os
import requests
import environ
from bs4 import BeautifulSoup
import jwt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

#Comment this if you wish to switch to Gemini Instead
from langchain_ollama import ChatOllama
#If you want to use gemini instead of ollama(local llm), uncomment this.
#from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pathlib import Path
from .models import WikiScrape, Quiz


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#Comment this if you want to switch to Gemini
model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0.9,
    base_url=env("OLLAMA_BASE_URL"),
)

#Uncomment this if you want to use Gemini Instead
# model = ChatGoogleGenerativeAI(
#     model="gemini-3-pro",
#     temperature=0.9,
#     api_key=env("GEMINI_API_KEY")
# )

system_message = SystemMessage(
    " \
    You are a data extraction assistant. Analyze the provided Wikipedia introduction and return JSON only. \
    Return keys in this exact order: 'quiz', 'key_entities', 'related_topics', 'summary'. \
    'quiz': Generate 3–4 MCQs with 4 options, 1 correct answer, and a brief explanation and the difficulty of the question (easy, medium or hard). \
    'key_entities': Must be a JSON object with keys 'people', 'organizations', 'locations'. \
    'related_topics': List 3–6 relevant topics from the text only. \
    'summary': Write a concise 2–3 sentence summary based strictly on the text. \
    Use ONLY the provided text. Do not add external knowledge. \
    Return ONLY valid JSON. No markdown, no filler text. \
    "

)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}



def scrape(url): 
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find(id="firstHeading").text
    
    # Get just the sub-header names (the 5 sections)
    sections = [span.text for span in soup.select('.mw-heading2 h2')][:5]
    
    table_info = soup.find('table',class_='infobox')

    results = {}

    if table_info:
    
        rows = table_info.find_all('tr')

        for row in rows:
            td = row.find('td', class_="infobox-data")
            th = row.find('th', class_="infobox-label")
            if td and th:
                key = th.text.strip()
                value = td.text.strip()
                final_value = value.replace("\n"," ")
                results[key]=final_value

    para = [p.text.strip() for p in soup.select(".mw-content-ltr p")][:5]
    
    # Context is now just a list of keywords
    context = {
        "title": title,
        "infobox": results,
        "sections": sections,
        "introduction": para
    }

    return context


def llm_response(text):
    human_message = HumanMessage(text)
    messages = [system_message, human_message]
    response = model.invoke(messages)
    return response.content


def session_token(payload):
    
    token = jwt.encode(payload, env("JWT_SECRET_TOKEN"), algorithm="HS256")
    return token 


#Registration
def add_user(*, username, password, email):
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return 409
    try:
        usr_object = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return usr_object
    except Exception:
        return 500

#Login
def check_user(*, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return user
    else:
        return 401
    

def add_wiki_quiz(*, user, url, scrape_data, ai_data):
    
    with transaction.atomic():
        wiki = WikiScrape.objects.create(
            user=user,
            url=url,
            title=scrape_data.get("title", ""),
            summary=ai_data.get("summary", ""),
            sections=scrape_data.get("sections", []),
            key_entities=ai_data.get("key_entities", {}),
            related_topics=ai_data.get("related_topics", [])
        )

        for q in ai_data.get("quiz", []):
            Quiz.objects.create(
                scrape=wiki,
                question=q["question"],
                options=q["options"],
                answer=q["answer"],
                difficulty=q.get("difficulty", Quiz.Difficulty.EASY),
                explanation=q["explanation"]
            )

    return wiki


def get_user_scrapes(*, user):
    scrapes = WikiScrape.objects.filter(user=user).order_by('-created_at')
    data = [
        {
            "id": s.id,
            "url": s.url,
            "title": s.title,
            "created_at": s.created_at.isoformat()
        }
        for s in scrapes
    ]
    return data


def get_scrape_detail(*, user, scrape_id):
    try:
        scrape = WikiScrape.objects.get(id=scrape_id, user=user)
        data = {
            "id": scrape.id,
            "url": scrape.url,
            "title": scrape.title,
            "summary": scrape.summary,
            "key_entities": scrape.key_entities,
            "sections": scrape.sections,
            "quiz": [
                {
                    "question": q.question,
                    "options": q.options,
                    "answer": q.answer,
                    "difficulty": q.difficulty,
                    "explanation": q.explanation
                }
                for q in scrape.quizzes.all()
            ],
            "related_topics": scrape.related_topics
        }
        return data
    except WikiScrape.DoesNotExist:
        return None