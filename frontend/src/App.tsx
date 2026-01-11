import { useState, useEffect } from 'react';
import './App.css';

interface QuizItem {
  question: string;
  options: string[];
  answer: string;
  difficulty: string;
  explanation: string;
}

interface ScrapeData {
  id: number;
  url: string;
  title: string;
  summary: string;
  key_entities: {
    people: string[];
    organizations: string[];
    locations: string[];
  };
  sections: string[];
  quiz: QuizItem[];
  related_topics: string[];
}

interface HistoryItem {
  id: number;
  url: string;
  title: string;
  created_at: string;
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentTab, setCurrentTab] = useState<'generate' | 'history'>('generate');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [quizData, setQuizData] = useState<ScrapeData | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [selectedQuiz, setSelectedQuiz] = useState<ScrapeData | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [loginData, setLoginData] = useState({ username: '', password: '', email: '' });
  const [isRegister, setIsRegister] = useState(false);
  const [authLoading, setAuthLoading] = useState(false);

  const API_BASE = 'http://localhost:8000/api';

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await fetch(`${API_BASE}/scrapes/`, {
        credentials: 'include'
      });
      if (response.ok) {
        setIsLoggedIn(true);
        const data = await response.json();
        setHistory(data);
      }
    } catch (error) {
      // Not logged in or error
    }
  };

  const handleLogout = async () => {
    try {
      // Clear local state
      setIsLoggedIn(false);
      setCurrentTab('generate');
      setUrl('');
      setQuizData(null);
      setHistory([]);
      setSelectedQuiz(null);
      setShowModal(false);
      setLoginData({ username: '', password: '', email: '' });
      
      // Clear cookies by making a request that will fail but clear session
      await fetch(`${API_BASE}/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCSRFToken() || '',
        },
      });
    } catch (error) {
      // Even if logout request fails, clear local state
      console.log('Logout completed locally');
    }
  };

  const getCSRFToken = () => {
    return document.cookie
      .split("; ")
      .find(row => row.startsWith("csrftoken="))
      ?.split("=")[1];
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthLoading(true);
    try {
      const endpoint = isRegister ? 'register' : 'login';
      
      // For registration, first make a GET request to get CSRF token
      if (isRegister) {
        await fetch(`${API_BASE}/register`, {
          method: 'GET',
          credentials: 'include',
        });
      }
      
      const body = isRegister
        ? { username: loginData.username, password: loginData.password, email: loginData.email }
        : { username: loginData.username, password: loginData.password };

      const response = await fetch(`${API_BASE}/${endpoint}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken() || '',
        },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        setIsLoggedIn(true);
        await checkAuth();
      } else {
        alert('Auth failed');
      }
    } catch (error) {
      alert('Error');
    }
    setAuthLoading(false);
  };

  const generateQuiz = async () => {
    if (!url) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/scrape`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken() || '',
        },
        body: JSON.stringify({ url }),
      });

      if (response.ok) {
        const data = await response.json();
        setQuizData(data);
        // Refresh history
        await checkAuth();
      } else {
        alert('Failed to generate quiz');
      }
    } catch (error) {
      alert('Error');
    }
    setLoading(false);
  };

  const loadQuizDetail = async (id: number) => {
    try {
      const response = await fetch(`${API_BASE}/scrapes/${id}/`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setSelectedQuiz(data);
        setShowModal(true);
      } else {
        alert('Failed to load details');
      }
    } catch (error) {
      alert('Error loading details');
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="auth-container">
        <h1>Wiki Quiz Generator</h1>
        <form onSubmit={handleAuth} className="auth-form">
          <h2>{isRegister ? 'Register' : 'Login'}</h2>
          <input
            type="text"
            placeholder="Username"
            value={loginData.username}
            onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
            required
          />
          {isRegister && (
            <input
              type="email"
              placeholder="Email"
              value={loginData.email}
              onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
              required
            />
          )}
          <input
            type="password"
            placeholder="Password"
            value={loginData.password}
            onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
            required
          />
          <button type="submit" disabled={authLoading}>
            {authLoading ? 'Loading...' : (isRegister ? 'Register' : 'Login')}
          </button>
          <button type="button" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Already have account? Login' : 'Need account? Register'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>Wiki Quiz Generator</h1>
        <nav>
          <button
            className={currentTab === 'generate' ? 'active' : ''}
            onClick={() => setCurrentTab('generate')}
          >
            Generate Quiz
          </button>
          <button
            className={currentTab === 'history' ? 'active' : ''}
            onClick={() => setCurrentTab('history')}
          >
            Past Quizzes
          </button>
          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Logout
          </button>
        </nav>
      </header>

      {currentTab === 'generate' && (
        <div className="generate-tab">
          <div className="input-section">
            <input
              type="url"
              placeholder="Enter Wikipedia URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={generateQuiz} disabled={loading}>
              {loading ? 'Generating...' : 'Generate Quiz'}
            </button>
          </div>
          {quizData && <QuizDisplay data={quizData} />}
        </div>
      )}

      {currentTab === 'history' && (
        <div className="history-tab">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>URL</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td>{item.title}</td>
                  <td><a href={item.url} target="_blank" rel="noopener noreferrer">{item.url}</a></td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                  <td>
                    <button onClick={() => loadQuizDetail(item.id)}>Details</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && selectedQuiz && (
        <div className="modal">
          <div className="modal-content">
            <button className="close" onClick={() => setShowModal(false)}>×</button>
            <QuizDisplay data={selectedQuiz} />
          </div>
        </div>
      )}
    </div>
  );
}

function QuizDisplay({ data }: { data: ScrapeData }) {
  return (
    <div className="quiz-display">
      <h2>{data.title}</h2>
      <p><strong>URL:</strong> <a href={data.url} target="_blank" rel="noopener noreferrer">{data.url}</a></p>
      <p><strong>Summary:</strong> {data.summary}</p>

      <div className="entities">
        <h3>Key Entities</h3>
        <p><strong>People:</strong> {data.key_entities.people.join(', ')}</p>
        <p><strong>Organizations:</strong> {data.key_entities.organizations.join(', ')}</p>
        <p><strong>Locations:</strong> {data.key_entities.locations.join(', ')}</p>
      </div>

      <div className="sections">
        <h3>Sections</h3>
        <ul>
          {data.sections.map((section, idx) => <li key={idx}>{section}</li>)}
        </ul>
      </div>

      <div className="quiz">
        <h3>Quiz</h3>
        {data.quiz.map((q, idx) => (
          <div key={idx} className="question-card">
            <h4>Question {idx + 1}: {q.question}</h4>
            <ul>
              {q.options.map((opt, i) => (
                <li key={i} className={opt === q.answer ? 'correct' : ''}>
                  {String.fromCharCode(65 + i)}. {opt}
                </li>
              ))}
            </ul>
            <p><strong>Difficulty:</strong> {q.difficulty}</p>
            <p><strong>Explanation:</strong> {q.explanation}</p>
          </div>
        ))}
      </div>

      <div className="related-topics">
        <h3>Related Topics</h3>
        <ul>
          {data.related_topics.map((topic, idx) => <li key={idx}>{topic}</li>)}
        </ul>
      </div>
    </div>
  );
}

export default App;
