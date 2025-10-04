# 🌍 Air Quality Monitor - Real-time Global Air Quality Dashboard

<div align="center">

![Air Quality Monitor](https://img.shields.io/badge/Air%20Quality-Monitor-blue?style=for-the-badge)
![NASA TEMPO](https://img.shields.io/badge/NASA-TEMPO-red?style=for-the-badge)
![Ambee API](https://img.shields.io/badge/Ambee-API-green?style=for-the-badge)

**A stunning, real-time air quality monitoring dashboard with NASA TEMPO satellite data integration and Ambee API support**

[Live Demo](#) • [Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation)

</div>

---

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Dashboards](#-dashboards)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

Air Quality Monitor is a comprehensive web-based application that provides real-time air quality data visualization across North America and globally. The platform integrates multiple data sources including NASA TEMPO satellite observations, Ambee real-time air quality API, and ground-based monitoring stations to deliver accurate, up-to-date air quality information.

### Key Highlights

- 🛰️ **NASA TEMPO Integration** - Hourly satellite-based air quality observations
- 🌐 **Global Coverage** - Real-time data from Ambee API for worldwide locations
- 🗺️ **Interactive Maps** - Click anywhere to get instant air quality data
- 📊 **Beautiful Visualizations** - Modern UI with animated charts and statistics
- ⚡ **Real-time Updates** - Live data with automatic refresh
- 🎨 **Stunning Design** - Glassmorphism effects, animated particles, and smooth transitions

---

## ✨ Features

### 🎯 Core Features

- **Real-time Air Quality Monitoring**
  - Live AQI (Air Quality Index) data
  - PM2.5, PM10, NO₂, O₃, SO₂, and CO measurements
  - Color-coded air quality categories (Good to Hazardous)

- **Interactive Map Interface**
  - Click-to-view pollution data for any location
  - Leaflet-based interactive maps
  - Geocoding integration for location names
  - Custom markers with AQI color coding

- **Multiple Data Sources**
  - NASA TEMPO satellite data
  - Ambee API real-time measurements
  - Fallback to simulated data for remote areas

- **Dynamic Visualizations**
  - Animated statistics counters
  - Staggered card animations
  - Floating particle effects
  - Gradient background animations
  - Glassmorphism UI elements

### 🏙️ City Monitoring

- Major cities across North America
- Real-time pollutant levels
- AQI categorization
- Country flags and location details

### 📱 Responsive Design

- Mobile-friendly interface
- Adaptive layouts
- Touch-optimized controls

---

## 🛠️ Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance Python web framework |
| **PostgreSQL + PostGIS** | Spatial database for geographic data |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic** | Data validation and settings |
| **HTTPX** | Async HTTP client for API calls |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Modern web standards |
| **JavaScript (ES6+)** | Interactive functionality |
| **Leaflet.js** | Interactive mapping library |
| **Chart.js** | Data visualization (optional) |
| **Next.js + React** | Advanced dashboard (Kerala/Ernakulam) |
| **TailwindCSS** | Utility-first CSS framework |

### APIs & Data Sources

- **NASA TEMPO** - Satellite air quality observations
- **Ambee API** - Real-time global air quality data
- **OpenStreetMap Nominatim** - Geocoding services
- **OpenStreetMap Tiles** - Map visualization

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancing

---

## 📁 Project Structure

```
NASA/
├── 📂 backend/                    # FastAPI backend server
│   ├── 📂 app/
│   │   ├── 📂 api/               # API endpoints
│   │   │   ├── cities.py         # City data endpoints
│   │   │   ├── summary.py        # Summary statistics
│   │   │   └── health.py         # Health check
│   │   ├── 📂 core/              # Core configuration
│   │   │   ├── config.py         # App settings
│   │   │   └── database.py       # Database connection
│   │   ├── 📂 models/            # Database models
│   │   │   ├── city.py           # City model
│   │   │   └── air_quality.py    # Air quality model
│   │   └── 📂 services/          # Business logic
│   │       └── air_quality.py    # AQ data processing
│   ├── 📂 data/                  # Data processing scripts
│   ├── 📂 ml/                    # Machine learning models
│   ├── main.py                   # Application entry point
│   └── requirements.txt          # Python dependencies
│
├── 📂 frontend/                   # Next.js frontend (advanced)
│   ├── 📂 components/            # React components
│   │   ├── AirQualityMap.tsx    # Map component
│   │   ├── AlertPanel.tsx       # Alerts component
│   │   ├── ForecastChart.tsx    # Chart component
│   │   └── ...
│   ├── 📂 pages/                # Next.js pages
│   │   ├── index.tsx            # Main dashboard
│   │   └── kerala.tsx           # Kerala-specific view
│   ├── 📂 styles/               # CSS styles
│   └── package.json             # Node dependencies
│
├── 📂 docker/                    # Docker configuration
│   ├── init-db.sql              # Database initialization
│   ├── init-kerala-db.sql       # Kerala DB setup
│   └── nginx.conf               # Nginx configuration
│
├── 📂 notebooks/                 # Jupyter notebooks
│   └── air_quality_pipeline_demo.ipynb
│
├── 🌐 dashboard-tempo.html       # ⭐ Main TEMPO dashboard (Ultra-modern)
├── 🌐 dashboard.html             # Alternative dashboard
├── 🌐 dashboard-modern.html      # Modern variant
│
├── 🐳 docker-compose.yml         # Main Docker setup
├── 🐳 docker-compose-kerala.yml  # Kerala-specific setup
├── 🐳 Dockerfile.backend         # Backend container
├── 🐳 Dockerfile.frontend        # Frontend container
│
├── 🚀 start.sh                   # Main startup script
├── 🚀 start-tempo.sh             # TEMPO dashboard startup
├── 🚀 start-kerala.sh            # Kerala dashboard startup
│
├── 📝 README.md                  # This file
├── 📝 API_DOCUMENTATION.md       # API reference
├── 📝 DEPLOYMENT.md              # Deployment guide
├── 📝 START_HERE_TEMPO.md        # TEMPO quick start
└── 📝 .env.example               # Environment variables template
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for Next.js frontend)
- **Docker & Docker Compose** (recommended)
- **PostgreSQL 13+** (if running without Docker)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd NASA
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start with Docker Compose**
   ```bash
   # Main dashboard
   docker-compose up -d
   
   # Or use the startup script
   chmod +x start-tempo.sh
   ./start-tempo.sh
   ```

4. **Access the dashboards**
   - **TEMPO Dashboard**: http://localhost:8000/dashboard-tempo.html
   - **Backend API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Next.js Frontend**: http://localhost:3000

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
# Create PostgreSQL database and update .env

# Run migrations (if applicable)
# alembic upgrade head

# Start the server
python main.py
```

#### Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Option 3: Quick Test

```bash
# Just open the HTML dashboard directly
cd NASA
python -m http.server 8080

# Then open: http://localhost:8080/dashboard-tempo.html
```

---

## 🎨 Dashboards

### 1. TEMPO Dashboard (Main) - `dashboard-tempo.html`

**Ultra-modern, feature-rich dashboard with:**
- ✨ Animated gradient background
- 🎆 Floating particle effects
- 💎 Glassmorphism UI elements
- 📊 Animated statistics counters
- 🗺️ Interactive Leaflet map
- 🌐 Ambee API integration
- 🛰️ NASA TEMPO data support

**Features:**
- Click anywhere on the map to get real-time air quality data
- Automatic fallback from Ambee API to simulated data
- Smooth animations and transitions
- Responsive design
- Live data updates

### 2. Kerala Dashboard - `frontend/pages/kerala.tsx`

**Regional dashboard for Kerala, India:**
- Specific to Ernakulam and surrounding areas
- Next.js/React implementation
- Advanced charting and forecasting
- Alert system integration

### 3. Classic Dashboard - `dashboard.html`

**Simple, lightweight dashboard:**
- Basic air quality display
- Minimal dependencies
- Fast loading
- Easy to customize

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### Get Summary Statistics

```http
GET /api/summary
```

**Response:**
```json
{
  "overall_aqi": 65,
  "aqi_category": "Moderate",
  "averages": {
    "pm25": 18.5,
    "pm10": 33.3,
    "no2": 22.1,
    "o3": 45.2,
    "so2": 8.3,
    "co": 0.6
  },
  "total_cities": 15,
  "cities": [...],
  "timestamp": "2025-10-04T15:30:00Z"
}
```

#### Get City Data

```http
GET /api/cities
```

#### Health Check

```http
GET /health
```

### Ambee API Integration

The dashboard integrates with Ambee API for real-time air quality data:

```javascript
// Endpoint: https://api.ambeedata.com/latest/by-lat-lng
// Headers: x-api-key: YOUR_API_KEY
```

**Configuration:**
Add your Ambee API key in `dashboard-tempo.html`:
```javascript
const AMBEE_API_KEY = 'your-api-key-here';
```

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/airquality
POSTGRES_USER=airquality_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=airquality

# API Keys
AMBEE_API_KEY=your_ambee_api_key_here
NASA_API_KEY=your_nasa_api_key_here

# Application
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
ENVIRONMENT=production

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Ambee API Key

1. Sign up at [Ambee Data](https://www.getambee.com/)
2. Get your API key from the dashboard
3. Add it to your `.env` file or directly in `dashboard-tempo.html`

### NASA TEMPO Data

NASA TEMPO data integration requires:
- NASA Earthdata account
- API credentials
- Data access permissions

See [START_HERE_TEMPO.md](START_HERE_TEMPO.md) for detailed setup.

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build and deploy
docker-compose -f docker-compose.yml up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

For production deployment guides, see [DEPLOYMENT.md](DEPLOYMENT.md)

**Deployment options:**
- AWS EC2 / ECS
- Google Cloud Run
- Azure App Service
- DigitalOcean Droplets
- Heroku
- Vercel (Frontend)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/TypeScript
- Write meaningful commit messages
- Add tests for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NASA TEMPO** - For satellite air quality data
- **Ambee** - For real-time air quality API
- **OpenStreetMap** - For mapping services
- **Leaflet.js** - For interactive maps
- **FastAPI** - For the amazing web framework

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/nasa-air-quality/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/nasa-air-quality/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ for cleaner air and better health**

⭐ Star this repo if you find it useful!

</div>
