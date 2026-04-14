# **BookGeek AI: hybrid book recommendation system**

<p align="center">
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"></a>
  <a href="https://scipy.org/"><img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy"></a>
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"></a>
  <a href="https://vitejs.dev/"><img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite"></a>
  <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
</p>

BookGeek AI is a **hybrid book recommendation system** combining **Collaborative Filtering (KNN-based)** and **Content-Based (TF-IDF + Cosine Similarity)** models, with a weighted hybrid approach for personalized results. The project ingests and preprocesses large-scale book datasets, applies active-user and popular-book filtering, and dynamically generates recommendations enriched with metadata (title, author, publisher, year, and cover image). I engineered a **modern, monolithic architecture** with separate **FastAPI JSON API** and **React (Tailwind/DaisyUI) Frontend**, ensuring scalability and maintainability. The system is fully containerized with **Docker**, featuring automated orchestration and a robust **CI/CD pipeline** with 100% backend test coverage and comprehensive frontend unit tests. This design demonstrates proficiency in **ML model building, asynchronous API development, modern SPA implementation, containerization, and industry-grade deployment workflows**.

---

## **Core Technologies**

| **Category**                | **Technology / Resource**                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| **Core Language**           | Python 3.11                                                                               |
| **Backend Framework**       | FastAPI                                                     |
| **Data Processing**         | Pandas (Data Cleaning & Merging), NumPy (Matrix Ops)                                      |
| **Recommendation Models**   | **Hybrid System**: Collaborative Filtering + Content-Based Filtering                      |
| **Collaborative Filtering** | SciPy (`csr_matrix`), scikit-learn (`NearestNeighbors`)                                   |
| **Content-Based Filtering** | scikit-learn (`TfidfVectorizer`, `cosine_similarity`)                                     |
| **Hybrid Fusion Logic**     | Weighted average score combination                                                        |
| **Data Sources**            | Book-Crossing Dataset (`BX-Books`, `BX-Users`, `BX-Ratings`)                              |
| **Feature Engineering**     | TF-IDF on combined features (`title`, `author`, `publisher`, `year`)                      |
| **Model Persistence**       | Pickle (Model & Processed Data Serialization)                                             |
| **Memory System**           | In-memory caching of processed data for faster responses                                  |
| **Evaluation Metrics**      | Popularity-based filtering, Active user filtering                                         |
| **Orchestration Layer**     | Modular service classes (`DataLoader`, `DataPreprocessor`, `ModelManager`, `HybridModel`) |
| **Frontend**                | React 19, Vite, Tailwind CSS, DaisyUI, Framer Motion                      |
| **Deployment**              | Docker (Python 3.11-slim base), `requirements.txt` dependency locking                     |
| **Portability**             | Pathlib-based cross-platform directory resolution                                         |
| **Error Handling**          | Graceful fallbacks & empty results handling                                               |

---

## **Comparison with Standard Systems**

| Feature | BookGeek AI | Typical Recommenders |
|---------|------------|----------------------|
| Method Flexibility | 3 modes + hybrid tuning | Usually single-method |
| Cold Start Handling | Popular books fallback | Often fails |
| Explainability | Shows scores + metadata | Black-box results |
| UI Customization | Adjustable weights/counts | Fixed parameters |

---

## **Project Structure**

```
Book-Geek/
├── .github/
│   └── workflows/
│       └── main.yml             # CI/CD Pipeline tracking tests and linting
|
├── backend/                     # FastAPI Backend service
│   ├── app/                     # Core application package
│   │   ├── core/                # Configuration and system-wide utilities
│   │   │   ├── config.py
│   │   │   ├── logger.py
│   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   ├── data/                # Raw book-crossing dataset (CSV)
│   │   │   ├── BX-Book-Ratings.csv
│   │   │   ├── BX-Books.csv
│   │   │   └── BX-Users.csv
│   │   ├── logs/                # Application runtime logs
│   │   │   └── app.log          # System execution log file
│   │   ├── models/              # Pickled ML models and processed data
│   │   │   ├── book_pivot.pkl
│   │   │   ├── books_content.pkl
│   │   │   ├── books_data.pkl
│   │   │   ├── cb_model.pkl
│   │   │   ├── cf_model.pkl
│   │   │   ├── content_sim_matrix.pkl
│   │   │   ├── final_rating.pkl
│   │   │   ├── tfidf_vectorizer.pkl
│   │   │   └── title_to_idx.pkl
│   │   ├── services/            # Recommendation engine components
│   │   │   ├── collaborative_model.py
│   │   │   ├── content_model.py
│   │   │   ├── data_loader.py
│   │   │   ├── data_preprocessor.py
│   │   │   ├── hybrid_model.py
│   │   │   ├── model_manager.py
│   │   │   ├── recommendation_engine.py
│   │   │   └── __init__.py
│   │   ├── main.py              # Application entry point (FastAPI)
│   │   └── train_models.py      # Script to retrain recommendation models
│   ├── tests/                   # Backend testing suite
│   │   ├── conftest.py
│   │   ├── test_collaborative_model.py
│   │   ├── test_config.py
│   │   ├── test_content_model.py
│   │   ├── test_data_loader.py
│   │   ├── test_data_preprocessor.py
│   │   ├── test_endpoints.py    # API endpoint tests (100% coverage)
│   │   ├── test_hybrid_model.py
│   │   ├── test_logger.py
│   │   ├── test_model_manager.py
│   │   ├── test_models.py
│   │   ├── test_recommendation_engine.py
│   │   └── __init__.py
│   ├── Dockerfile               # Backend containerization
│   ├── pyproject.toml           # Backend build and lint config
│   ├── requirements.txt         # Backend Python dependencies
│   ├── run.py                   # Service-level runner
│   └── setup.py                 # Backend package installation
|
├── frontend/                    # React SPA (Vite + Tailwind + DaisyUI)
│   ├── public/                  # Public static assets
│   ├── src/                     # Source code
│   │   ├── components/          # Reusable UI components
│   │   │   ├── Background.js
│   │   │   ├── BookCard.js
│   │   │   ├── BookCard.test.js # Frontend unit tests
│   │   │   ├── Hero.js
│   │   │   └── Hero.test.js
│   │   ├── App.css
│   │   ├── App.js               # Main application logic
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   └── setupTests.js        # Vitest environment setup
│   ├── Dockerfile               # Multi-stage production build (Nginx)
│   ├── package.json             # Frontend dependencies and scripts
│   ├── tailwind.config.js       # UI Design configuration
│   ├── vite.config.js           # Frontend build tool config
│   └── vitest.config.js         # Frontend testing configuration
|
├── notebooks/                   # Research and experimental notebooks
│   └── experiment.ipynb         
|
├── .gitignore                   # Project-wide ignore rules
├── docker-compose.yml   
├── LICENSE   
├── README.md                    # Project documentation
├── render.yml                   # Production deployment config
└── run.py                       # local runner for backend and frontend
```

---

## **Architecture Diagram (Mermaid)**
```mermaid
graph TD
    A[Raw Data: BX-Books, BX-Users, BX-Ratings] --> B[Data Preprocessing & Feature Engineering]
    B --> C[Collaborative Filtering Model]
    B --> D[Content-Based Model]
    
    C --> E[User-Item Matrix - csr_matrix]
    D --> F[TF-IDF Features - Title+Author+Publisher+Year]
    
    E --> G[Hybrid Recommender - Weighted Score Fusion]
    F --> G
    
    G --> H[FastAPI JSON API - Endpoints for Recommendations]
    H --> I[Frontend: React SPA + Tailwind/DaisyUI]
    
    subgraph Deployment
        J[Docker Compose Orchestration]
        J --> H
        J --> I
    end
    
    G --> K[Model Persistence - Pickle Serialization]
```

---

## Quick Start (Automated)

### Prerequisites

- Python 3.10+
- Node.js & npm

### One-Click Setup & Run

The project includes an intelligent launcher that automatically handles dependency installation for both the backend and frontend.

```bash
# Clone the repository
git clone https://github.com/TanishqArora01/Book-Geek.git
cd Book-Geek

# Run the automated setup and launcher
python run.py
```

> [!TIP]
> The script will automatically detect if `node_modules` or Python packages are missing and install them for you before starting the services.

### Running the Application

#### **Local Development (Simultaneous)**
Use the unified local runner at the project root to start both services:
```bash
cd Book-Geek
python run.py
```
*   **Backend**: `http://127.0.0.1:8000`
*   **Frontend**: `http://localhost:5173` (with API proxy to 8000)

#### **Individual Services**
```bash
# Backend only
cd backend && python run.py

# Frontend only
cd frontend && npm run dev
```

---

## API Endpoints (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/popular` | Get popular books (JSON) |
| POST | `/api/recommend` | Get book recommendations (JSON) |
| GET | `/api/search_books` | Search books by title (JSON) |
| GET | `/api/health` | Health check endpoint |

## Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Testing & Quality Assurance

### Backend (Pytest)
```bash
# Run all backend tests
cd backend && pytest tests/ -v

# Run with coverage (100% Target)
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Frontend (Vitest)
```bash
# Run all frontend tests
cd frontend && npm test

# Run with coverage
npm run test:coverage
```

### CI/CD Pipeline
Our GitHub Actions pipeline (`.github/workflows/main.yml`) automatically performs the following on every push:
1. **Linting**: flake8 and isort for backend, ESLint for frontend.
2. **Backend Testing**: Runs full suite with 100% coverage requirement.
3. **Frontend Testing**: Runs Vitest suite for component integrity.
4. **Docker Build**: Verifies that both services build correctly.

---
  
**Prepared by:**  

**Tanishq**  
**Email:** [aroratanishq54@gmail.com](mailto:aroratanishq54@gmail.com)

