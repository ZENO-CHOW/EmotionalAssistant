# 🌱 Xiao An — Emotional Management Assistant for College Students

An MVP DBT-based emotional first-aid system powered by the DeepSeek API.

## Quick Start

### 1. Configure Environment Variables

Copy the environment-variable template and configure it:

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file and fill in the required settings:

**Main configuration options**:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database URL | `sqlite:///./data/emotions.db` |
| `LLM_API_KEY` | DeepSeek API key | - |
| `LLM_BASE_URL` | DeepSeek API base URL | `https://api.deepseek.com` |
| `LLM_MODEL` | DeepSeek model name | `deepseek-chat` |
| `VISION_API_KEY` | Vision-model API key | - |
| `VISION_BASE_URL` | Vision-model API base URL | `https://api.siliconflow.cn/v1` |
| `VISION_MODEL` | Vision-model name | `Qwen/Qwen3-VL-30B-A3B-Instruct` |

### 2. Install Dependencies

**Frontend dependencies**:

```bash
cd frontend && npm install
```

**Backend dependencies**:

```bash
cd backend && pip install -r requirements.txt
```

### 3. Start the Services

**Start the backend server**:

```bash
cd backend && python start_backend.py
```

The backend starts at http://localhost:8000.

**Start the frontend development server** (in a new terminal):

```bash
cd frontend && npm run dev
```

The frontend starts at http://localhost:8080.

### 4. Open the Web App

Visit the following URLs in your browser:

- User portal: http://localhost:8080
- Admin portal: http://localhost:8080/admin

**Administrator account**:

Username: `admin`
Password: `admin123`

## Project Structure

```
.
├── frontend/              # Vue.js frontend project
│   ├── src/               # Frontend source code
│   ├── index.html         # HTML entry point
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite configuration
├── backend/               # Python FastAPI backend
│   ├── app/               # Backend application source code
│   ├── .env               # Environment-variable configuration
│   ├── requirements.txt   # Python dependencies
│   └── start_backend.py   # Backend startup script
└── README.md              # Documentation
```

## Tech Stack

- **Frontend**: Vue.js 3 + Vite
- **Backend**: Python + FastAPI
- **Database**: SQLite
- **AI**: DeepSeek API
- **Design**: Liquid glass with a forest-green theme

## Features

### Completed

- ✅ Real-time chat (integrated with DeepSeek)
- ✅ Quick emotion selection (anxiety, sadness, anger, and emptiness)
- ✅ Conversation history (in-memory storage)
- ✅ Journal display (static example)
- ✅ Personal profile (static example)
- ✅ Database persistence
- ✅ User authentication
- ✅ Real journal entries
- ✅ Emotion-data analytics

### Planned

- ⏳ Crisis detection and referral

## API Endpoints

### POST /api/chat

Send a message to Xiao An.

**Request**:

```json
{
  "message": "I feel very anxious",
  "userId": "default" // Optional
}
```

**Response**:

```json
{
  "message": "It sounds like you're having a really difficult time right now...",
  "success": true
}
```

### POST /api/clear

Clear conversation history.

**Request**:

```json
{
  "userId": "default"
}
```

### GET /api/health

Health check.

## Development Notes

### Development Mode (Auto Restart)

```bash
npm run dev
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | - |
| `DEEPSEEK_API_URL` | API URL | `https://api.deepseek.com/v1/chat/completions` |
| `DEEPSEEK_MODEL` | Model name | `deepseek-chat` |

## Xiao An's Persona

- **Role**: An AI assistant dedicated to helping college students cope with emotional difficulties
- **Style**: Conversational, warm, and friend-like
- **Approach**: Based on DBT (Dialectical Behavior Therapy)
- **Principles**: Empathy first, preserve user choice, and acknowledge limitations

## Important Notice

⚠️ **Do not use this for an actual mental-health crisis**:

- It cannot replace professional mental-health care.
- If you are in crisis, please contact a professional crisis hotline.

## License

MIT
