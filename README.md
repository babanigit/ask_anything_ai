# Ask Anything AI - Django Backend

A lightweight, high-performance, and containerized Django-based REST API serving as the AI assistant backend for [Aniket Panchal's Portfolio Website](https://pixelify-porfolio-ts.vercel.app/). It integrates with OpenRouter to power both a context-restricted portfolio chatbot and a general developer assistant.

---

## 🚀 Key Features

- **Context-aware Portfolio AI (`/api/personalPortfolio/ask/`)**: An AI chatbot that dynamically answers professional queries about Aniket Panchal's work experience, education, certificates, skills, and projects. Its answers are strictly bound to structured JSON portfolio data to prevent hallucination.
- **Developer Assistant API (`/api/ai/ask/`)**: A coding assistant helper designed to analyze, fix, and optimize code while suggesting developer best practices in a structured markdown response format.
- **Modular Service Architecture**: Decoupled service layer utilizing OpenRouter APIs, enabling clean service logic separation and easy switching between LLM models (e.g., NVIDIA Nemotron, GPT models).
- **Prompt Engineering**: Custom system prompts and builders optimized for different AI use cases (developer assistant vs. context-bound portfolio AI).
- **Dockerized Deployment**: Fully containerized setup, CORS pre-configured, and served with Gunicorn for reliable production deployment.
- **Status & Health Check (`/api/status/`, `/api/test/`)**: Simple ping/pong endpoints to check service availability.

---

## 📁 Directory Structure

```text
├── core/                       # Main Django project configuration (settings, routing, WSGI/ASGI)
├── api/                        # Health check and basic test app
├── ai/                         # Developer/Code AI assistant app
├── personalPortfolio/          # App specifically handling portfolio-based AI chat
├── services/                   # Service layer for third-party integrations
│   ├── get_gists.py            # Fetches and caches Aniket's structured portfolio details
│   ├── openai_service.py       # Interacts with OpenRouter for developer questions
│   └── personal_portfolio_ai_service.py # Interacts with OpenRouter for portfolio context
├── prompts/                    # System prompts and prompt builders
│   ├── dev_prompt.py           # Structuring inputs and output formatting for developers
│   └── personal_portfolio_prompts.py # Context instructions and rules for the portfolio AI
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Container definition for deployability
└── db.sqlite3                  # Local SQLite database
```

---

## 🛠️ Tech Stack

- **Framework**: [Django 6.0+](https://djangoproject.com/)
- **WSGI HTTP Server**: [Gunicorn](https://gunicorn.org/)
- **AI SDK & Client**: Custom `requests`-based client configured for [OpenRouter API](https://openrouter.ai/)
- **Containerization**: [Docker](https://www.docker.com/)
- **Security/CORS**: `django-cors-headers` (configured for cross-origin frontend communication)

---

## ⚙️ Environment Configuration

To run this project, create a `.env` file in the `core/` directory:

```env
SECRET_KEY="your-django-secret-key"
ENVIRONMENT="development" # or "production"
PRODUCTION_DOMAIN="https://ask-anything-ai.onrender.com/api/"

# OpenRouter Configuration
OPENROUTER_API_KEY="your-openrouter-api-key"
OPENROUTER_URL="https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL="nvidia/nemotron-3-super-120b-a12b:free" # or any other model
```

---

## 🏃 Getting Started

### Method 1: Local Development

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/babanigit/ask_anything_ai.git
    cd ask_anything_ai
    ```

2.  **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations**:

    ```bash
    python manage.py migrate
    ```

5.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/`.

---

### Method 2: Docker Setup

1.  **Build the Docker image**:

    ```bash
    docker build -t ask-anything-ai-backend .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8000:8000 --env-file core/.env ask-anything-ai-backend
    ```
    The application will start, serving the endpoints through Gunicorn at port `8000`.

---

## 🔌 API Reference

### 1. Health / Status Check

- **Endpoint**: `/api/status/` or `/api/test/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": true,
    "message": "Success"
  }
  ```

---

### 2. Developer AI Assistant

- **Endpoint**: `/api/ai/ask/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "language": "python",
    "intent": "Explain list comprehension",
    "input": "How can I filter even numbers from a list in Python?",
    "history": []
  }
  ```
- **Response**:
  ````json
  {
    "success": true,
    "message_ai_response": "Explanation:\nList comprehension allows you to filter and transform lists concisely.\n\nCode:\n```python\nevens = [x for x in numbers if x % 2 == 0]\n```\n\nTips:\n- Use for simple transformations only.\n- Use generator expressions for large data sets.",
    "payload_for_ref": "{\"model\": \"nvidia/nemotron-3-super-120b-a12b:free\", ...}",
    "payload_message_length_for_ref": 3,
    "total_chat_history_for_ref": [
      {
        "role": "user",
        "content": "..."
      }
    ]
  }
  ````

---

### 3. Personal Portfolio Chatbot

- **Endpoint**: `/api/personalPortfolio/ask/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "input": "What projects has Aniket built?",
    "history": "[]"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Aniket has built several projects, including:\n1. **Finshark**: A real-time stock tracking platform built using ASP.NET Core, React.js, TypeScript, PostgreSQL, and Docker.\n2. **Multiplayer Tic-Tac-Toe**: A real-time game platform built using TypeScript, Node.js, Express, MongoDB, and React.",
    "history": "[{\"role\": \"user\", \"content\": \"What projects has Aniket built?\"}, {\"role\": \"assistant\", \"content\": \"Aniket has built several projects...\"}]"
  }
  ```

---

## 🔐 System Rules for Portfolio AI

The portfolio assistant uses a dedicated system prompt configuration to guarantee precision and truthfulness:

1.  **Context-Bound**: The chatbot answers _only_ using details present in the fetched portfolio schema (Gist / Cache).
2.  **No Hallucinations**: It does not invent skills, experience, or certifications. If information is missing, it responds: `"That information is not available in the portfolio."`
3.  **Domain Restriction**: Questions unrelated to Aniket's profile will be politely deflected with a message indicating the assistant's professional purpose.

---

## 🚧 Roadmap & Future Plans

The project is an active work-in-progress. The next phases of development focus on:
- ✨ **More AI Endpoints**: Adding dedicated endpoints for other projects and applications under development.
- 🧠 **Smarter Context Handling**: Improving prompt chaining and memory retention for richer conversational context.
- 🔌 **Reusable AI Services**: Refactoring the service layer into pluggable modules that can easily be integrated into future applications.
- 🔒 **Security Hardening**: Enhancing authentication, rate limiting, and input validation prior to public release.
