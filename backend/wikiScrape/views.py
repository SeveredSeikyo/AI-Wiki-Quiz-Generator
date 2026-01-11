from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import json
import datetime
from .utils import scrape, llm_response, session_token, add_user, check_user, add_wiki_quiz, get_user_scrapes, get_scrape_detail


# Create your views here.

@ensure_csrf_cookie
@require_POST
def register(request):

    try:
        data = json.loads(request.body)
        username = data.username
        password = data.password.encode('utf-8')
        email = data.password

        if not all ([username,password,email]):
            return JsonResponse({"error": "Missing Fields"}, status=400)

        result = add_user(
            username=username, 
            password=password, 
            email=email
        )
        if result == 409:
            return JsonResponse({"error": "User already exists"}, status=409)

        if result == 500:
            return JsonResponse({'error': 'An Internal Error Occurred'}, status=500)


        payload = {
            "user_id": result.email,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        }

        token = session_token(payload)

        response = JsonResponse({"message": "User Registration Successful"}, status=201)

        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=86400
        )

        return response

    except Exception:
        return JsonResponse({'error': 'An Internal Error Occurred'}, status=500)


@ensure_csrf_cookie
@require_POST
def login(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        result = check_user(
            username=username, 
            password=password
        )

        if result == 401:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        payload = {
            "user_id": result.email,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        }

        token = session_token(payload)

        response = JsonResponse({"message": "User Authorized Successful"}, status=201)

        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=86400
        )

        return response
    except Exception:
        return JsonResponse({"error": "Internal Server Error"}, status=500)



@login_required
@require_POST
def scrape_wiki(request):
    try:
        body = json.loads(request.body)
        url = body.get("url")

        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        #Scrape Wikipedia
        scrape_data = scrape(url)

        #Send structured data to LLM
        llm_input = json.dumps(scrape_data, ensure_ascii=False)
        llm_output = llm_response(llm_input)

        #Parse AI JSON
        ai_data = json.loads(llm_output)

        #Save to DB
        wiki = add_wiki_quiz(
            user=request.user,
            url=url,
            scrape_data=scrape_data,
            ai_data=ai_data
        )

        response_data = {
            "id": wiki.id,
            "url": wiki.url,
            "title": wiki.title,
            "summary": wiki.summary,
            "key_entities": wiki.key_entities,
            "sections": wiki.sections,
            "quiz": [
                {
                    "question": q.question,
                    "options": q.options,
                    "answer": q.answer,
                    "difficulty": q.difficulty,
                    "explanation": q.explanation
                }
                for q in wiki.quizzes.all()
            ],
            "related_topics": wiki.related_topics
        }

        return JsonResponse(response_data, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON from AI"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_GET
def get_scrapes(request):
    data = get_user_scrapes(user=request.user)
    return JsonResponse(data, safe=False)


@login_required
@require_GET
def get_scrape_detail(request, scrape_id):
    data = get_scrape_detail(user=request.user, scrape_id=scrape_id)
    if data is None:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse(data)
