# Wiki Quiz Generator

A full-stack web application that scrapes Wikipedia articles and generates AI-powered quizzes using Large Language Models (LLMs).

## Features

### Core Functionality
- **User Authentication**: Register and login system with JWT tokens
- **Wikipedia Scraping**: Extracts article content, sections, and metadata
- **AI Quiz Generation**: Uses LangChain with Ollama or Google Gemini to create multiple-choice questions
- **Quiz Management**: Store and retrieve generated quizzes from database
- **Responsive UI**: Clean, modern interface with tabbed navigation

### Quiz Features
- 3-4 multiple choice questions per article
- Difficulty levels (easy, medium, hard)
- Detailed explanations for each answer
- Related Wikipedia topics suggestions
- Key entities extraction (people, organizations, locations)

## Tech Stack

### Backend
- **Framework**: Django 5.2.10
- **Database**: PostgreSQL
- **Authentication**: JWT tokens with CSRF protection
- **Scraping**: BeautifulSoup4
- **AI Integration**: LangChain with Ollama (local LLM) or Google Gemini
- **API**: RESTful endpoints

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: CSS3 with responsive design
- **HTTP Client**: Fetch API with CSRF token handling

## Project Structure

```
Deepklarity/
├── backend/                 # Django backend
│   ├── backendApi/         # Django project settings
│   ├── wikiScrape/         # Main app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API endpoints
│   │   ├── utils.py        # Business logic & AI integration
│   │   ├── urls.py         # URL routing
│   │   └── migrations/     # Database migrations
│   ├── requirements.txt    # Python dependencies
│   ├── manage.py          # Django management script
│   └── backend.http       # API testing requests
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   ├── App.css        # Styling
│   │   └── main.tsx       # App entry point
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite configuration
│   └── frontend.md        # Frontend documentation
├── objective.md           # Project requirements
└── README.md             # This file
```

## Prerequisites

### Backend
- Python 3.8+
- PostgreSQL database
- Ollama (for local LLM) or Google Gemini API key

### Frontend
- Node.js 16+
- npm or yarn

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # Windows
   # source myenv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create `.env` file in backend directory:
   ```env
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   DB_HOST=localhost
   DB_PORT=5432
   JWT_SECRET_TOKEN=your_jwt_secret_key
   OLLAMA_BASE_URL=http://localhost:11434
   # GEMINI_API_KEY=your_gemini_api_key  # Uncomment if using Gemini
   ```

5. **Set up database:**
   - Create PostgreSQL database
   - Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start Ollama (if using local LLM):**
   ```bash
   # Install and start Ollama
   # Pull the model: ollama pull qwen3:1.7b
   ```

7. **Run the server:**
   ```bash
   python manage.py runserver
   ```
   Server will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Quiz Operations
- `POST /api/scrape` - Generate quiz from Wikipedia URL
- `GET /api/scrapes/` - Get user's quiz history
- `GET /api/scrapes/<id>/` - Get detailed quiz data

## Usage

1. **Register/Login** through the frontend
2. **Generate Quiz Tab:**
   - Enter a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Alan_Turing`)
   - Click "Generate Quiz"
   - View the generated quiz with questions, answers, and explanations
3. **Past Quizzes Tab:**
   - View table of previously generated quizzes
   - Click "Details" to view full quiz in modal

## Configuration

### Switching LLM Models

In `backend/wikiScrape/utils.py`:

**For Ollama (default):**
```python
model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0.9,
    base_url=env("OLLAMA_BASE_URL"),
)
```

**For Google Gemini:**
```python
model = ChatGoogleGenerativeAI(
    model="gemini-3-pro",
    temperature=0.9,
    api_key=env("GEMINI_API_KEY")
)
```

### Database Configuration

Update `.env` file with your PostgreSQL credentials.

## Development

### Running Tests
```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm test
```

### Code Quality
- Backend: Follow Django best practices
- Frontend: Use TypeScript for type safety
- All model operations in `utils.py`, views only call utilities

## Deployment

### Backend (Django)
- Use Gunicorn for production
- Configure PostgreSQL in production
- Set `DEBUG=False` and proper `SECRET_KEY`

### Frontend (React)
- Build for production: `npm run build`
- Deploy to Vercel, Netlify, or any static hosting

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper commit messages
4. Test thoroughly
5. Submit pull request

## License

This project is for educational purposes. Check individual component licenses.

## Support

For issues or questions, please check the code comments or create an issue in the repository.