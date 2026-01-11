# Frontend Documentation

This is the React frontend for the Wiki Quiz Generator application.

## Overview

The frontend provides a clean, responsive user interface for:
- User authentication (login/register)
- Quiz generation from Wikipedia URLs
- Viewing past generated quizzes
- Interactive quiz display with explanations

## Tech Stack

- **React 18** with TypeScript
- **Vite** for build tooling
- **CSS3** for styling
- **Fetch API** for HTTP requests
- **CSRF token handling** for Django backend integration

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main application component
│   ├── App.css          # Global styles and responsive design
│   ├── main.tsx         # Application entry point
│   └── assets/          # Static assets (React/Vite logos)
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite build configuration
├── eslint.config.js     # ESLint configuration
└── frontend.md          # This documentation
```

## Features

### Authentication
- Login/Register forms with validation
- CSRF token extraction from cookies
- Automatic authentication state management

### Quiz Generation
- URL input with validation
- Real-time loading states
- Structured quiz display with:
  - Article metadata (title, summary, sections)
  - Key entities extraction
  - Multiple choice questions
  - Answer explanations
  - Related topics suggestions

### Quiz History
- Table view of past quizzes
- Modal popup for detailed quiz view
- Fetches data from backend API

### UI/UX
- Responsive design for mobile and desktop
- Tabbed navigation
- Clean card-based layout
- Highlighted correct answers
- Modal dialogs for detailed views

## Installation

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

The application will run on `http://localhost:5173` and proxy API calls to `http://localhost:8000`.

## Configuration

### API Base URL
The API base URL is configured in `App.tsx`:
```typescript
const API_BASE = 'http://localhost:8000/api';
```

### CSRF Token Handling
The frontend automatically extracts CSRF tokens from cookies:
```typescript
const getCSRFToken = () => {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
};
```

All POST requests include the CSRF token in headers.

## Component Structure

### App Component
Main component handling:
- Authentication state
- Tab navigation
- API calls
- Modal management

### QuizDisplay Component
Reusable component for displaying quiz data:
- Article information
- Quiz questions and answers
- Related topics

## API Integration

### Authentication Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Quiz Endpoints
- `POST /api/scrape` - Generate quiz from URL
- `GET /api/scrapes/` - Get quiz history
- `GET /api/scrapes/<id>/` - Get detailed quiz

All requests include `credentials: 'include'` for cookie handling.

## Styling

The application uses custom CSS with:
- CSS variables for consistent theming
- Flexbox and Grid for layouts
- Responsive breakpoints
- Hover states and transitions
- Modal overlays

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

### TypeScript Configuration

- Strict type checking enabled
- React JSX support
- ES2020 target

### ESLint Configuration

- React and TypeScript rules
- Import sorting
- Code formatting standards

## Browser Support

- Modern browsers with ES6+ support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## CORS Configuration

For development, ensure the Django backend allows CORS from `http://localhost:5173`. Add to Django settings:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

## Deployment

### Build for Production
```bash
npm run build
```

This creates optimized files in the `dist/` directory that can be deployed to any static hosting service.

### Environment Variables
For production deployment, you may need to configure the API base URL as an environment variable.

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure backend allows frontend origin
2. **CSRF token missing**: Check that backend sets `csrftoken` cookie
3. **API connection failed**: Verify backend is running on port 8000

### Development Tips

- Use browser dev tools to inspect network requests
- Check console for TypeScript errors
- Test on multiple screen sizes for responsiveness

## Contributing

When making changes to the frontend:
1. Follow TypeScript best practices
2. Maintain responsive design
3. Test API integration thoroughly
4. Update this documentation if needed