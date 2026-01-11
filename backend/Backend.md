# Backend Documentation

This Django project provides a backend API for scraping Wikipedia pages, generating AI-powered quizzes, summaries, and related data using local LLMs (Ollama) or Google Gemini. It includes user authentication and data persistence.

## Project Structure

- **backendApi/**: Main Django project configuration.
- **wikiScrape/**: App handling scraping, models, views, and utilities.
- **requirements.txt**: Python dependencies.
- **.env**: Environment variables (see `.env.example` for template).
- **backend.http**: Example HTTP requests for testing.
- **vercel.json**: Vercel deployment configuration.
- **api/index.py**: Vercel serverless function entry point.

## Deployment

### Vercel Deployment

This backend is configured for deployment on Vercel. The `vercel.json` file contains the deployment configuration, and `api/index.py` serves as the serverless function entry point.

#### Prerequisites

1. **PostgreSQL Database**: Since Vercel doesn't provide PostgreSQL, you need to set up an external database service such as:
   - [Neon](https://neon.tech)
   - [Supabase](https://supabase.com)
   - [Railway](https://railway.app)
   - [ElephantSQL](https://www.elephantsql.com)

2. **Environment Variables**: Set the following in your Vercel project settings:
   - All variables from `.env.example`
   - Database connection details for your external PostgreSQL service
   - `DEBUG=False` for production
   - `ALLOWED_HOSTS` including your Vercel domain

#### Deployment Steps

1. Push your code to GitHub.
2. Connect your GitHub repository to Vercel.
3. Set environment variables in Vercel dashboard.
4. Deploy.

The API will be available at `https://your-project.vercel.app/api/`.

## Environment Variables

Configure the following in `.env` (based on `.env.example`):

- `DB_USERNAME`: Database username.
- `DB_PASSWORD`: Database password.
- `DB_NAME`: Database name.
- `DB_HOST`: Database host.
- `DB_PORT`: Database port.
- `OLLAMA_BASE_URL`: Base URL for Ollama LLM (e.g., `http://localhost:11434`).
- `GEMINI_API_KEY`: API key for Google Gemini (optional, if switching from Ollama).
- `JWT_SECRET_TOKEN`: Secret for JWT token generation.
- `FRONTEND_URL`: Frontend URL for CORS allowed origins (e.g., `http://localhost:5173`).
- `DEBUG`: Set to `True` for development, `False` for production.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (e.g., `localhost,127.0.0.1,.vercel.app`).

## Models

### WikiScrape
- `user`: ForeignKey to User.
- `url`: URLField.
- `title`: CharField (max 255).
- `summary`: TextField.
- `sections`: JSONField (list of section names).
- `key_entities`: JSONField (dict with 'people', 'organizations', 'locations').
- `related_topics`: JSONField (list of topics).
- `created_at`: DateTimeField (auto_now_add).

### Quiz
- `scrape`: ForeignKey to WikiScrape.
- `question`: TextField.
- `options`: JSONField (list of 4 options).
- `answer`: CharField (correct answer).
- `difficulty`: CharField (choices: 'easy', 'medium', 'hard').
- `explanation`: TextField.

## API Endpoints

All endpoints are prefixed with `/api/`. Authentication uses JWT tokens in cookies.

### POST /api/register
Registers a new user.

**Request Body (JSON):**
```json
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

**Response (Success, 201):**
```json
{
  "message": "User Registration Successful"
}
```
Sets `access_token` cookie.

**Errors:**
- 400: Missing fields.
- 409: User already exists.
- 500: Internal error.

### POST /api/login
Logs in a user.

**Request Body (JSON):**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (Success, 201):**
```json
{
  "message": "User Authorized Successful"
}
```
Sets `access_token` cookie.

**Errors:**
- 401: Unauthorized.
- 500: Internal server error.

### POST /api/scrape
Scrapes a Wikipedia URL, generates AI data, and saves to DB. Requires authentication.

**Request Body (JSON):**
```json
{
  "url": "https://en.wikipedia.org/wiki/Example"
}
```

**Response (Success, 201):**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Example",
  "title": "Example Title",
  "summary": "Concise 2-3 sentence summary.",
  "key_entities": {
    "people": ["Person1"],
    "organizations": ["Org1"],
    "locations": ["Location1"]
  },
  "sections": ["Section1", "Section2"],
  "quiz": [
    {
      "question": "Question?",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "difficulty": "easy",
      "explanation": "Explanation."
    }
  ],
  "related_topics": ["Topic1", "Topic2"]
}
```

**Errors:**
- 400: URL required.
- 500: Invalid JSON from AI or other errors.

## Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`.
2. Set up PostgreSQL database and configure `.env`.
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`.
4. Start server: `python manage.py runserver`.
5. (Optional) Switch LLM in `wikiScrape/utils.py` by commenting/uncommenting model imports.

## Example Usage

Use `backend.http` in VS Code or tools like REST Client for testing. Example scrape request as shown.
