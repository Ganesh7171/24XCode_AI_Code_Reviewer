# AI Code Reviewer

A production-ready AI-powered code review system using **Retrieval-Augmented Generation (RAG)** and **AWS Bedrock**. This application analyzes source code against company coding standards, identifies issues, suggests improvements, and provides refactored code with detailed explanations.

![AI Code Reviewer](https://img.shields.io/badge/AI-Code%20Reviewer-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

## 🚀 Features

### Core Functionality
- **RAG Pipeline**: Retrieves relevant coding standards using FAISS vector database
- **AI-Powered Review**: Uses AWS Bedrock (Claude 3) for intelligent code analysis
- **Comprehensive Feedback**: Provides issues, risks, improvements, refactored code, and explanations
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust

### Technical Features
- **FastAPI Backend**: High-performance async API with rate limiting
- **React Frontend**: Modern, responsive UI with Tailwind CSS
- **Vector Search**: FAISS for efficient similarity search
- **Embeddings**: AWS Bedrock Titan or HuggingFace fallback
- **Docker Support**: Complete containerization with Docker Compose
- **Security**: Input validation, rate limiting, API key protection

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher (for frontend development)
- **Docker & Docker Compose**: For containerized deployment
- **AWS Account**: With Bedrock access (Claude 3 and Titan Embeddings)

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **LLM**: AWS Bedrock (Claude 3 Sonnet)
- **Embeddings**: AWS Bedrock Titan / HuggingFace
- **Vector DB**: FAISS
- **RAG**: LangChain

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Syntax Highlighting**: react-syntax-highlighter

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx (production)

## 📁 Project Structure

```
ai-code-reviewer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── rag/
│   │   ├── loader.py          # Document loader
│   │   ├── embedder.py        # Embedding generator
│   │   └── retriever.py       # FAISS retriever
│   ├── llm/
│   │   └── reviewer.py        # Code reviewer
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── Dockerfile            # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.jsx          # Main application
│   │   ├── api.js           # API client
│   │   └── index.css        # Styles
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── tailwind.config.js   # Tailwind configuration
│   ├── nginx.conf           # Nginx configuration
│   └── Dockerfile           # Frontend container
├── standards/
│   └── sample_rules.md      # Sample coding standards
├── docker-compose.yml       # Docker orchestration
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-code-reviewer
   ```

2. **Configure environment variables**
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   Edit `.env` and add your AWS credentials:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
   BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1
   ```

3. **Start the application**
   ```bash
   cd ..
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

5. **Run the backend**
   ```bash
   python main.py
   ```
   Backend will run on http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## 📖 Usage

### 1. Upload Coding Standards (Optional)

- Click "Upload Standards" button
- Upload `.md` or `.txt` files with your coding standards
- The system will index them for RAG retrieval

### 2. Submit Code for Review

1. **Select Language**: Choose your programming language
2. **Add Description**: Provide a brief description of the code
3. **Paste Code**: Enter the code you want reviewed
4. **Click "Review Code"**: Submit for AI analysis

### 3. Review Results

The system provides:
- **Issues**: Bugs, errors, and standard violations
- **Risks**: Potential security or performance risks
- **Improvements**: Suggested enhancements
- **Refactored Code**: Improved version with syntax highlighting
- **Explanation**: Detailed reasoning for changes

## 🔧 API Endpoints

### Health Check
```http
GET /health
```

### Review Code
```http
POST /review-code
Content-Type: application/json

{
  "code": "def example():\n    pass",
  "description": "Example function",
  "language": "python"
}
```

### Upload Standards
```http
POST /upload-standards
Content-Type: application/json

{
  "content": "# Coding Standards\n...",
  "source": "company_standards"
}
```

### Reload Standards
```http
POST /reload-standards
```

## 🔐 Security

- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: 10 requests per minute per IP
- **Environment Variables**: Secrets stored in `.env` (not committed)
- **CORS**: Configured for specific origins in production
- **File Upload**: Size limits and type validation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Performance

- **RAG Retrieval**: < 100ms for similarity search
- **LLM Response**: 2-5 seconds (depends on code complexity)
- **Concurrent Requests**: Supports async processing
- **Vector Index**: Optimized with FAISS

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: AWS Bedrock authentication error
```bash
# Verify AWS credentials in .env
# Ensure IAM user has Bedrock permissions
```

**Issue**: FAISS index not found
```bash
# The index will be created automatically on first run
# Ensure standards/ directory has .md or .txt files
```

### Frontend Issues

**Issue**: `npm install` fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: API connection refused
```bash
# Ensure backend is running on port 8000
# Check vite.config.js proxy settings
```

## 🚢 Deployment

### Production Considerations

1. **Environment Variables**: Use secrets management (AWS Secrets Manager, etc.)
2. **CORS**: Update allowed origins in `main.py`
3. **HTTPS**: Use reverse proxy (Nginx, Traefik) with SSL
4. **Scaling**: Use load balancer for multiple backend instances
5. **Monitoring**: Add logging, metrics (Prometheus, CloudWatch)

### Docker Production Build

```bash
docker-compose -f docker-compose.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- AWS Bedrock for LLM capabilities
- LangChain for RAG framework
- FastAPI for backend framework
- React team for frontend framework

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: your-email@example.com

---

**Built with ❤️ using RAG, AWS Bedrock, FastAPI, and React**
