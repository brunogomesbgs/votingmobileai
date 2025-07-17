# votingmobileai
# Feature Voting Application

A full-stack application for posting and voting on feature requests, built with React Native (Expo) frontend and FastAPI backend.

## Features

- **Create Features**: Users can post new feature requests with title, description, and author name
- **Vote on Features**: Users can vote on existing features (one vote per user per feature)
- **Real-time Updates**: Vote counts update in real-time
- **Responsive Design**: Works on mobile and web platforms
- **Error Handling**: Comprehensive error handling and user feedback
- **Unit Tests**: Full test coverage for both frontend and backend

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for Python
- **Tortoise ORM**: Async ORM for Python
- **Pydantic**: Data validation using Python type annotations
- **MySQL**: Database for persistent storage
- **Docker**: Containerization

### Frontend
- **React Native**: Cross-platform mobile development
- **Expo**: Development platform for React Native
- **Axios**: HTTP client for API calls
- **React Navigation**: Navigation library

## Project Structure

```
feature-voting-app/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── models.py
│   └── test_main.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── App.js
│   ├── babel.config.js
│   ├── app.json
│   ├── src/
│   │   ├── screens/
│   │   │   ├── CreateFeatureScreen.js
│   │   │   └── VoteScreen.js
│   │   └── services/
│   │       └── apiService.js
│   └── __tests__/
│       └── components.test.js
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js (for local development)
- Python 3.12+ (for local development)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone git@github.com:brunogomesbgs/votingmobileai.git
   cd votingmobileai
   ```

2. **Create the directory structure**
   ```bash
   mkdir -p backend frontend/src/screens frontend/src/services frontend/__tests__
   ```

3. **Copy the provided files to their respective locations**

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Features
- `POST /features` - Create a new feature
- `GET /features` - Get all features
- `GET /features/{id}` - Get a specific feature

### Votes
- `POST /votes` - Vote for a feature

### Health
- `GET /health` - Health check endpoint

## Testing

### Backend Tests
```bash
cd backend
pytest test_main.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Database Schema

### Features Table
- `id` (INT, PRIMARY KEY)
- `title` (VARCHAR(255))
- `description` (TEXT)
- `created_by` (VARCHAR(100))
- `created_at` (DATETIME)
- `vote_count` (INT)

### Votes Table
- `id` (INT, PRIMARY KEY)
- `feature_id` (INT, FOREIGN KEY)
- `voter_id` (VARCHAR(100))
- `created_at` (DATETIME)
- Unique constraint on (`feature_id`, `voter_id`)

## Error Handling

The application includes comprehensive error handling:
- Input validation using Pydantic
- Duplicate vote prevention
- Network error handling
- User-friendly error messages
- Graceful degradation

## Security Features

- Input sanitization
- SQL injection prevention through ORM
- CORS configuration
- Error message sanitization
- Rate limiting considerations

## Future Enhancements

- User authentication system
- Feature categories and tags
- Comment system
- Admin panel
- Push notifications
- Feature status tracking
- Advanced sorting and filtering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.