# Aether Intelligence Platform 🌌

**The Enterprise-Grade Semantic Codebase Search & Intelligence Platform.**

Aether is a next-generation code intelligence system that combines vector retrieval, graph theory, and multi-agent AI to provide deep semantic understanding of massive software repositories.

## ✨ Core Features

- **Semantic Ingestion Engine**: Distributed pipeline for indexing millions of lines of code across GitHub, GitLab, and local monorepos.
- **Graph-Based Code Reasoning**: Automatically builds dependency graphs, call graphs, and architecture maps using Tree-sitter AST analysis.
- **Autonomous Research Agents**: AI agents powered by LangGraph that can explore repositories, trace execution flows, and identify architectural bottlenecks.
- **Cinematic UI/UX**: High-performance dashboard with interactive 2D/3D dependency visualizations.
- **Hybrid Retrieval Engine**: Combines keyword search with semantic embeddings for sub-second accurate results.

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Framer Motion, D3.js, React Flow.
- **Backend**: FastAPI (Python), SQLAlchemy, Celery, RabbitMQ.
- **Data**: Qdrant (Vector DB), PostgreSQL (Metadata), Redis (Cache).
- **AI**: OpenAI GPT-4o, Text-Embedding-3, LangGraph, Tree-sitter.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aether-intelligence/platform.git
   cd platform
   ```

2. Setup environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API Key
   ```

3. Spin up the infrastructure:
   ```bash
   docker-compose -f infra/docker/docker-compose.yml up -d
   ```

4. Start development servers:
   ```bash
   # Backend
   cd apps/api
   pip install -r requirements.txt
   uvicorn main:app --reload

   # Frontend
   cd apps/web
   npm install
   npm run dev
   ```

## 📐 Architecture

Aether follows a microservices architecture designed for horizontal scalability:

- **Ingestion Worker**: Clones and walks repos.
- **Parsing Service**: Extracts symbols and metadata using Tree-sitter.
- **Embedding Pipeline**: Generates high-dimensional vectors for semantic search.
- **Graph Service**: Maintains the repository knowledge graph in NetworkX.
- **Intelligence API**: Orchestrates AI agents and provides the search interface.

---

Built for elite engineers. Designed for the future of software development.
