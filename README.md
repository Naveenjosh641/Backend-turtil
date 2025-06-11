"""
# Resume-Role Fit Evaluator

A production-ready FastAPI microservice that evaluates how well a candidate's resume fits a specific job role and provides personalized learning recommendations.

## Features

- **Resume-Job Matching**: AI-powered scoring using TF-IDF and cosine similarity
- **Skill Extraction**: Intelligent extraction and normalization of technical skills
- **Learning Path Generation**: Personalized step-by-step learning recommendations
- **Offline Operation**: Fully offline with no external API dependencies
- **Production Ready**: Async FastAPI with proper error handling, logging, and validation
- **Dockerized**: Complete containerization for easy deployment

## API Endpoints

### POST /api/v1/evaluate-fit
Evaluate resume-job fit and generate learning recommendations.

**Request:**
```json
{
    "resume_text": "I've worked on Django apps, SQL databases, and basic cloud deployments. Familiar with Python scripting and Flask.",
    "job_description": "We are hiring backend engineers with expertise in Node.js, MongoDB, containerized deployments (Docker), and AWS. Bonus for experience in system design."
}
```

**Response:**
```json
{
    "fit_score": 0.46,
    "verdict": "moderate_fit",
    "matched_skills": ["Python", "Cloud Basics"],
    "missing_skills": ["Node.js", "MongoDB", "Docker", "AWS", "System Design"],
    "recommended_learning_track": [
        {
            "skill": "Node.js",
            "steps": [
                "Install Node.js and learn basic syntax",
                "Understand asynchronous programming in JS",
                "Build a REST API with Express.js",
                "Handle authentication and routing"
            ]
        }
    ],
    "status": "success"
}
```

### GET /api/v1/health
Health check endpoint.

### GET /api/v1/version
Get service version information.

## Installation & Setup

### Local Development

1. **Clone and Setup**
```bash
git clone <repository>
cd resume-fit-evaluator
pip install -r requirements.txt
```

2. **Create Environment**
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. **Run the Service**
```bash
python main.py
```

The service will be available at `http://localhost:8000`

### Docker Deployment

1. **Build Image**
```bash
docker build -t resume-fit-evaluator .
```

2. **Run Container**
```bash
docker run -p 8000:8000 resume-fit-evaluator
```

## Configuration

### Skills Configuration (data/skills.json)
Define skill categories and aliases for accurate extraction and normalization.

### Learning Paths (data/learning_paths.json)
Define step-by-step learning paths for each skill.

### Application Config (data/config.json)
Configure fit score thresholds, skill aliases, and other application settings.

## Architecture

The application follows a clean, modular architecture:

```
app/
├── api/
│   └── routes.py          # FastAPI routes and endpoints
├── core/
│   ├── config.py          # Application configuration
│   └── logging_config.py  # Logging setup
├── models/
│   └── schemas.py         # Pydantic models and validation
├── services/
│   ├── fit_engine.py      # Main evaluation engine
│   ├── skill_extractor.py # Skill extraction logic
│   ├── scoring_engine.py  # Similarity scoring
│   └── learning_path_generator.py # Learning recommendations
data/
├── skills.json           # Skills and aliases configuration
├── learning_paths.json   # Learning path definitions
└── config.json          # Application configuration
```

## Testing

### Manual Testing Examples

1. **Strong Fit (Score > 0.7)**
```bash
curl -X POST "http://localhost:8000/api/v1/evaluate-fit" \
-H "Content-Type: application/json" \
-d '{
    "resume_text": "Senior Python developer with 5 years Django experience, PostgreSQL database design, AWS cloud deployments, Docker containerization, and Git version control",
    "job_description": "Python developer needed with Django, PostgreSQL, AWS, and Docker experience"
}'
```

2. **Moderate Fit (Score 0.4-0.7)**
```bash
curl -X POST "http://localhost:8000/api/v1/evaluate-fit" \
-H "Content-Type: application/json" \
-d '{
    "resume_text": "I have worked with Python and SQL databases, some cloud experience",
    "job_description": "Backend engineer with Node.js, MongoDB, Docker, AWS, and system design expertise"
}'
```

3. **Weak Fit (Score < 0.4)**
```bash
curl -X POST "http://localhost:8000/api/v1/evaluate-fit" \
-H "Content-Type: application/json" \
-d '{
    "resume_text": "Frontend developer with HTML, CSS, and basic JavaScript",
    "job_description": "Senior backend engineer with Node.js, MongoDB, Docker, Kubernetes, AWS, microservices, and system design"
}'
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Production Deployment

### Environment Variables
```bash
DEBUG=false
LOG_LEVEL=info
SKILLS_FILE=data/skills.json
LEARNING_PATHS_FILE=data/learning_paths.json
CONFIG_FILE=data/config.json
```

### Docker Compose Example
```yaml
version: '3.8'
services:
  resume-evaluator:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Features Implementation

### Skill Extraction
- Uses regex pattern matching with word boundaries
- Normalizes skills using configurable aliases
- Supports fuzzy matching for skill variations

### Scoring Algorithm
- **Skill Matching (70%)**: Direct skill overlap ratio
- **Text Similarity (30%)**: TF-IDF cosine similarity
- **Verdict Thresholds**: 
  - Strong Fit: ≥ 0.7
  - Moderate Fit: 0.4 - 0.69
  - Weak Fit: < 0.4

### Learning Path Generation
- Maps missing skills to predefined learning tracks
- Supports configurable maximum steps per skill
- Falls back to generic learning paths for unknown skills

## Logging

Logs are written to both console and `logs/app.log`:
- Application startup/shutdown events
- Request processing information
- Error tracking and debugging
- Performance metrics

## Error Handling

- **Input Validation**: Pydantic models with custom validators
- **Service Errors**: Graceful error handling with appropriate HTTP status codes
- **Global Exception Handler**: Catches unhandled exceptions
- **Health Checks**: Built-in health monitoring

## Performance Considerations

- **Async Operations**: Full async/await support
- **Memory Efficient**: In-memory caching of configuration data
- **Fast Startup**: Lazy loading of ML models
- **Scalable**: Stateless design for horizontal scaling

## Security Features

- **Input Sanitization**: Text validation and cleaning
- **CORS Support**: Configurable cross-origin requests
- **Rate Limiting**: Ready for production rate limiting
- **No Data Persistence**: Stateless operation for security

## Monitoring

- **Health Endpoint**: `/api/v1/health` for uptime monitoring
- **Version Endpoint**: `/api/v1/version` for deployment tracking
- **Structured Logging**: JSON-formatted logs for monitoring tools
- **Docker Health Checks**: Built-in container health monitoring

## Future Enhancements

- **Machine Learning Models**: Integration with sentence transformers
- **Skill Ontology**: Hierarchical skill relationships
- **Industry-Specific**: Domain-specific skill sets and paths
- **Real-time Updates**: Dynamic skill and learning path updates
- **Analytics**: Usage metrics and improvement suggestions

## License

This project is licensed under the MIT License.
"""
