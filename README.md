# Cariboun AI - Intelligent Chat Assistant with ESG Reporting

## 🌟 Overview

Cariboun AI is a sophisticated chat application that leverages OpenAI's GPT-4 to provide intelligent conversations with built-in ESG (Environmental, Social, and Governance) report generation. The application features a modern Vue.js frontend with a FastAPI backend, offering real-time streaming responses, conversation history management, and PDF report generation.

## ✨ Key Features

- **🤖 Intelligent AI Conversations**: Real-time chat with OpenAI's GPT-4
- **📊 ESG Report Generation**: Generate comprehensive ESG reports from conversations
- **🎯 Streaming Responses**: Live streaming of AI responses
- **💬 Conversation Management**: Thread-based chat history with sidebar navigation
- **📁 PDF Export**: Download ESG reports as professional PDF documents
- **🌙 Dark/Light Mode**: User-friendly theme switching
- **🚫 Rate Limit Handling**: Graceful handling of OpenAI rate limits with user notifications
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

```
Frontend (Vue.js 3)
├── Chat Interface
├── Real-time Streaming
├── Toast Notifications
└── PDF Download

Backend (FastAPI + PostgreSQL)
├── OpenAI Integration
├── Thread Management
├── ESG Report Generation
└── PDF Creation

Database (PostgreSQL)
├── Users
├── Threads
├── Messages
└── PDF Attachments
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **Node.js 16+**
- **PostgreSQL 13+**
- **OpenAI API Key** (from [OpenAI Platform](https://platform.openai.com/))
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/erf04/CaribounAI.git
cd CaribounAI
```

### 2. Environment Setup

1. Copy the .env.example file to the .env file should look like this:
```bash
cp .env.example .env
```

the .env file in project root:
```
OPENAI_API_KEY=<your_openai_api_key>
OPENAI_ASSISTANT_ID=<your_assistant_id>
DATABASE_URL=postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PASS>@<POSTGRES_HOST>:<POSTGRES_PORT>/esgbuddy
POSTGRES_PASS=<your_secure_password>
```
then paste your values for the corresponding keys
2. in the frontend directory , create a .env file :
```
touch frontend/.env
```
and set VITE_API_BASE_URL variable in it :
```
VITE_API_BASE_URL=/api
```

### 3. Project Structure
```
project/
├── backend/          # FastAPI application
├── frontend/         # Vue.js application
    ├── src/  
    ├── nginx/
    ├── .env
    ...              
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docker-bake.hcl
├── .env
└── .env.example
```

### 4. Deploy Application

`notice` : because of github CI/CD disabled , We use docker-compose.dev.yml to dockerize the project for now that requires the whole source code . if the CI/CD is up and working , use docker-compose.prod.yml only (doesn't need to deploy the source code on the server).
```
# Build and start all services
docker compose -f docker-compose.dev.yml up --build -d
# Verify services are running(you should see backend , frontend and postgres services up and running)
docker compose -f docker-compose.dev.yml ps
```


### 5. Access Application

 - Frontend: http://your_server_ip:80

 - Backend API: http://your_server_ip:8000

 - API Docs: http://your_server_ip:8000/docs

 - Database: your_server_ip:5432

## 🔧 Detailed Configuration

### OpenAI Assistant Setup

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to "Assistants" section
3. Create a new assistant or use an existing one
4. Copy the Assistant ID and add it to your `.env` file

### Database Schema

The application uses the following main tables:

- **users**: User authentication and profiles
- **threads**: Conversation threads per user
- **messages**: Individual chat messages
- **pdf_attachments**: Generated ESG reports

### Rate Limit Configuration

The application handles OpenAI rate limits by:

1. Detecting rate limit errors in responses
2. Showing user-friendly toast notifications
3. Suggesting users start new conversations
4. Preventing further API calls until new conversation starts

## 📁 Project Structure

```
cariboun-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── chat.py          # Chat endpoints
│   │   │   │   └── threads.py
│   │   │   └── routers.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── models.py            # Database models
│   │   │   └── init_db.py
│   │   ├── schemas/
│   │   │   └── message.py
│   │   └── services/
│   │       ├── auth.py
│   │       ├── openai_service.py    # OpenAI integration
│   │       └── pdf.py               # PDF generation
│   ├── alembic/
│   │   └── versions/                # Database migrations
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Chat.vue             # Main chat component
    │   ├── stores/
    │   │   └── auth.js              # Pinia store
    │   ├── router/
    │   │   └── index.js
    │   └── main.js
    ├── public/
    ├── package.json
    └── .env.example
```

## 🛠️ Development


### Building for Production

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m db.init_db

# Frontend
cd frontend
npm run build
```



## 🔍 API Documentation

### Authentication Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Chat Endpoints

- `POST /chat/stream` - Stream chat responses
- `GET /chat/{thread_id}/messages` - Get thread messages
- `GET /chat/generate-esg-report` - Generate ESG report
- `GET /chat/download-pdf/{message_id}` - Download PDF report

### Thread Endpoints

- `GET /threads` - Get user threads
- `POST /threads/new` - Create new thread
- `DELETE /threads/{thread_id}` - Delete thread

## 🎨 Frontend Features

### Chat Interface Components

1. **Sidebar Navigation**
   - User profile display
   - Conversation history
   - Collapsible design

2. **Chat Area**
   - Real-time message display
   - Markdown rendering
   - Message actions (copy, regenerate)

3. **Input Area**
   - Smart textarea with auto-resize
   - Enter-to-send functionality
   - Character count

4. **Toast Notifications**
   - Rate limit warnings
   - Success/error messages
   - Auto-dismiss with progress bar

### Rate Limit Handling Flow

```mermaid
graph TD
    A[User sends message] --> B[Backend calls OpenAI]
    B --> C{Check rate limit}
    C -->|Rate limit exceeded| D[Return rate limit error]
    C -->|Within limits| E[Return AI response]
    D --> F[Frontend shows toast]
    F --> G[Suggest new conversation]
    E --> H[Display response]
```

## 📝 Usage Guide

### Starting a Conversation

1. Login to the application
2. Click "New Chat" in the sidebar
3. Type your message in the input box
4. Press Enter to send

### Generating ESG Reports

1. Have a conversation about your company
2. Click "Generate ESG Report" button in header
3. Wait for report generation
4. Download PDF from chat

### Managing Conversations

- **View History**: Click on conversation in sidebar
- **Delete Conversation**: Click delete button on active conversation
- **Switch Themes**: Click moon/sun icon in sidebar

## 🐛 Troubleshooting

### Common Issues

1. **"Rate limit exceeded" errors**
   - Start a new conversation
   - Wait a few minutes before trying again
   - Consider upgrading OpenAI plan

2. **Database connection issues**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify DATABASE_URL in .env file
   - Ensure database exists: `psql -l`

3. **Frontend not connecting to backend**
   - Verify VITE_API_BASE_URL in frontend .env
   - Check CORS settings in backend
   - Ensure both servers are running



## 🔒 Security Considerations

1. **API Keys**: Never commit .env files to version control
2. **Authentication**: JWT tokens with expiration
3. **CORS**: Configured to allow only specific origins
4. **Rate Limiting**: Implemented at application level
5. **Input Validation**: Sanitize user inputs

## 📈 Performance Optimization

### Backend
- Use connection pooling for database
- Implement response caching
- Optimize OpenAI API calls

### Frontend
- Lazy load components
- Implement virtual scrolling for long chats
- Optimize bundle size with code splitting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



## 🙏 Acknowledgments

- OpenAI for the GPT-4 API
- Vue.js and FastAPI communities
- All contributors and testers

## 📞 Support

For issues and questions:
- Open a GitHub Issue
- Check the Wiki for documentation
- Email: erfan.ka.004@gmail.com

---

**Happy Coding! 🚀**
