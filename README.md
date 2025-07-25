<!-- # COSMO_Digitals-BE

Backend API for COSMO Digitals built with FastAPI and MongoDB.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB (local or cloud)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd COSMO_Digitals-BE
   ```

2. **Set up virtual environment**
   
   **Option A: Using PowerShell (Recommended)**
   ```powershell
   .\activate_venv.ps1
   ```
   
   **Option B: Manual activation**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Option C: Using Command Prompt**
   ```cmd
   activate_venv.bat
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with:
   ```env
   mongo_uri=mongodb://localhost:27017
   MONGO_DB_NAME=my_fastapi_db
   smtp_host=smtp.gmail.com
   smtp_port=587
   smtp_username=your_email@gmail.com
   smtp_password=your_app_password
   smtp_use_tls=true
   notify_email=your_email@gmail.com
   default_from_email=your_email@gmail.com
   ```

5. **Run the application**
   ```bash
   python run.py
   ```
   
   Or with auto-reload:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📁 Project Structure

```
COSMO_Digitals-BE/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   │   └── config.py
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── services/
├── venv/                 # Virtual environment
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── README.md
```

## 🔧 Development

### Virtual Environment Management

- **Activate:** `.\venv\Scripts\Activate.ps1` (PowerShell) or `activate_venv.bat` (CMD)
- **Deactivate:** `deactivate`
- **Install new package:** `pip install package_name`
- **Update requirements:** `pip freeze > requirements.txt`

### API Endpoints

- `POST /contact/` - Submit contact form
- `GET /docs` - API documentation (Swagger UI)

## 🛠️ Technologies Used

- **FastAPI** - Modern web framework
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment variable management
- **Email-validator** - Email validation

## 📝 Notes

- The project uses a virtual environment to isolate dependencies
- All packages are installed locally in the `venv` directory
- No global Python packages are required
- The application uses dataclasses instead of pydantic for data validation -->
