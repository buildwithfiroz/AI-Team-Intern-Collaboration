# 📊 Dynamic Review Analytics

## 📌 Overview  
**Dynamic Review Analytics** is a full-stack application that scrapes, analyzes, and visualizes product data.  
It empowers users to:  
- Scrape product details & reviews from e-commerce sites  
- Store and process structured/unstructured data  
- Display insights dynamically on an interactive dashboard  

The backend is built with **Flask (Python)** using **Blueprints** for modular routing, while the frontend dashboards integrate real-time data for user-friendly insights.  

---

## 🛠 Tech Stack  

- **Backend:** Python, Flask, Flask-Blueprints  
- **Frontend/Dashboard: ** html , js , tailwind , jinja template  *
- **Database:** SQLite / PostgreSQL / MySQL *(initially setup, later switched to JSON storage)*  
- **Libraries & Tools:** Pandas, NumPy, Requests, BeautifulSoup / Selenium  

---

## 📂 Project Structure  

```bash
Dynamic-Review-Analysis
├── main
│   ├── app.py
│   ├── config.py
│   ├── database
│   │   ├── connection.py
│   │   └── dra.db
│   ├── routes
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── dashboard.py
│   │   ├── home.py
│   │   ├── input_url.py
│   │   ├── login.py
│   │   ├── logout.py
│   │   └── signup.py
│   ├── src
│   │   └── amazon_scraper.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── images
│   │   │   ├── banner.png
│   │   │   ├── favicon.png
│   │   │   └── image.png
│   │   ├── reviews.json
│   │   └── script
│   │       ├── charts.js
│   │       ├── chatbot.js
│   │       └── script.js
│   ├── templates
│   │   ├── base.html
│   │   ├── chat.html
│   │   ├── dashboard.html
│   │   ├── index.html
│   │   ├── input_url.html
│   │   ├── landing.html
│   │   ├── login.html
│   │   └── signup.html
│   └── utils
│       └── cleaner.py
├── README.md
└── requirements.txt


⚡ Features
✅ Modular Blueprint-based routing
✅ Scalable folder structure for maintainability
✅ REST API endpoints for dashboard data
✅ Data fetching & integration into dashboards
✅ Collaboration-ready backend setup



👥 Team Contributions
Romman Khan
Designed scalable folder structure
Implemented routes using Flask Blueprints
Set up backend app factory
Integrated database setup (later switched to JSON as per team decision)
helped Nehal in data fetching for dashboards


🔮 Future Improvements
Switch back to a relational database for scalability
Add authentication with JWT / OAuth
Implement unit tests & CI/CD pipeline
Improve API documentation with Swagger / OpenAPI



