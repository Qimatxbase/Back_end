# News Aggregator + Data Visualization Project

A full-stack data pipeline application that scrapes news articles from NewsAPI and The Guardian, stores data into MongoDB Atlas, and provides a backend API + React frontend for visualization and analysis.

---

## Requirements

* Python 3.13 (recommended 3.11)
* Node.js 18+ with npm
* MongoDB Atlas account (with a database and user configured)

### Backend Python requirements (Back\_end/requirements.txt)

```txt
requests
python-dotenv
flask
requests
beautifulsoup4
pandas
flask_cors
pymongo
```

---

## Backend Setup (Python + Flask)

1. **Clone repository & go to backend folder:**

```bash
cd Back_end
```

2. **Create virtual environment:**

```bash
python -m venv venv
```

3. **Activate virtual environment:**

```bash
# On Windows
venv\Scripts\activate
```

4. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

5. **Configure .env file:**

```ini
NEWS_API_KEY=your_newsapi_key
GUARDIAN_API_KEY=your_guardianapi_key
MONGODB_URI=mongodb+srv://Qimatx:Qimatx@qimatx.tvk44wn.mongodb.net/
MONGODB_DBNAME=Qimatx
```

6. **Run backend server:**

```bash
python app.py
```

Backend available at: [http://localhost:5000](http://localhost:5000)

---

## Frontend Setup (React)

1. **Go to frontend folder:**

```bash
cd Front_end
```

2. **Install npm dependencies:**

```bash
npm install
```

3. **Run React development server:**

```bash
npm start
```

Frontend available at: [http://localhost:3000](http://localhost:3000)

---
## Testing

```bash
pytest tests/test_all.py

---

## Fully Terminal-Based Workflow (No VS Code needed)

You can run the entire project using any terminal:

```bash
# Backend
cd Back_end
venv\Scripts\activate
python app.py

# Frontend
cd Front_end
npm install
npm start
```

---

## Project Structure

```
Final_Project/
├── Back_end/      # Python Flask backend + MongoDB Handler
├── Front_end/     # React frontend visualization
├── modules/       # Custom Python modules
├── requirements.txt
├── README.md
```

---

## Notes

* Project works best with MongoDB Atlas cloud database.
* All data (category + keyword) are normalized to lowercase and no spaces.
* Recommended test environment: local + personal hotspot.

---

**This project was fully built and tested without using Visual Studio Code. All setup can be done entirely from terminal.**
