
# Pittsburgh Test Project

This is a **FastAPI-based web application** designed as a test project to demonstrate the integration of a FastAPI backend with PostgreSQL, Docker, and Alembic for database migrations. The project is fully containerized using Docker and supports development and production environments.

---

## **Project Structure**

The project is structured as follows:

```
Pittsburgh-Test-Project/
├── logs/                     # Directory for application logs
├── scripts/                  # Shell scripts for tasks like starting the app
├── src/                      # Source code
│   ├── apps/                 # Application modules
│   ├── db/                   # Database models and migrations
│   ├── media/                # Static/media files
│   ├── fastapi_core.py       # Core FastAPI app setup
│   ├── logging_conf.py       # Logging configuration
│   ├── runner.py             # Application entry point
│   ├── settings.py           # Application settings
├── .env                      # Environment variables
├── alembic.ini               # Alembic configuration
├── docker-compose.yml        # Docker Compose setup
├── Dockerfile                # Dockerfile for the web service
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/pittsburgh-test-project.git
cd Pittsburgh-Test-Project
```

### **2. Environment Setup**

1. **Create an `.env` file** by copying `.env-example`:
   ```bash
   cp .env-example .env
   ```

2. Update the `.env` file with your environment-specific settings:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=yourdatabase
   APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:yourpassword@db:5432/yourdatabase
   ```

### **3. Build and Run with Docker**

Ensure Docker and Docker Compose are installed on your machine.

1. Build the Docker containers:
   ```bash
   docker-compose build
   ```

2. Run the containers:
   ```bash
   docker-compose up
   ```

3. Access the application at:
   ```
   http://localhost:8000
   ```

### **4. Database Migrations**

1. To generate a new migration:
   ```bash
   docker exec -it fast_app alembic revision --autogenerate -m "Your migration name"
   ```

2. To apply migrations:
   ```bash
   docker exec -it fast_app alembic upgrade head
   ```

---

## **Development Workflow**

### **Local Development**

1. Install dependencies in a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the application locally:
   ```bash
   uvicorn src.runner:main_app --reload
   ```

3. Access the application at:
   ```
   http://localhost:8000
   ```

### **Linting and Formatting**
This project uses `black` for code formatting. Run:
```bash
black .
```

---

## **Features**

- **FastAPI Backend**: A lightweight, high-performance Python web framework.
- **PostgreSQL Database**: A relational database integrated via `asyncpg` and SQLAlchemy.
- **Alembic Migrations**: Manage schema changes in a structured way.
- **Dockerized Environment**: Fully containerized using Docker and Docker Compose for ease of deployment.
- **Logging**: Configurable logging setup for better observability.

---

## **Contributing**

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to the branch.
4. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

