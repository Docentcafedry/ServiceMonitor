# ServiceMonitor 🛠️

ServiceMonitor is a web-based tool to monitor the status and performance of your services and servers in real-time. It provides dashboards, and historical metrics to help you ensure uptime and reliability.

---

## Features

- Monitor multiple services simultaneously (HTTP, TCP, etc.)
- Real-time status updates
- Web dashboard for visual monitoring
- Docker support for easy deployment

---

## Technology Stack

- Backend: Python
- Frontend: React.js
- Database: PostgreSQL / SQLite
- Containerization: Docker & Docker Compose
- Web server: Nginx

---

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Docentcafedry/ServiceMonitor.git
cd ServiceMonitor
```

2. Build and start containers:
```bash

docker-compose up --build -d
```

3. Open your browser and navigate to: 

http://localhost:80


### Manual Setup

1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Install Node.js dependencies:
```bash
cd client
npm install
```

3. Start backend server:
```bash
cd backend
uvicorn main:app --reload --port 8080
```
4. Start React app:
```bash
cd client
npm run dev
```

5. Access the web dashboard at:
http://localhost:5174

