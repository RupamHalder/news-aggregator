# News Aggregator with Sentiment Analysis

This is a Python-based Flask application that aggregates news articles from multiple sources using the NewsAPI and
includes a sentiment analysis feature to determine the tone of each article. Users can filter news by categories, save
favorite articles, and personalize their dashboard.

---

## Features

- Aggregate news articles from multiple sources using NewsAPI.
- Filter articles by categories like tech, politics, sports, etc.
- Perform sentiment analysis to display the tone (positive, neutral, negative) of each article.
- User-friendly interface with AJAX-powered content loading.
- Save favorite articles and topics to a personalized dashboard.
- Dynamically load sources and articles without reloading the page.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- Virtualenv

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/news-aggregator.git
   cd news-aggregator

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Set Up NewsAPI Key**:
    * Sign up at [NewsAPI](https://newsapi.org/) and get your API key.
    * Create a file named `app_credentials.json` in the project root directory and add your API key and other details:
       ```bash
        {
            "SECRET_KEY": "your_flask_app_secret_here",
            "NEWS_API_KEY": "your_api_key_here",
            "DB_NAME": "your_database_name_here",
            "DB_USERNAME": "your_database_username_here",
            "DB_PASSWORD": "your_database_password_here",
            "DB_HOST": "your_database_host_here"
        }
   
5. **Run the Application**:
   ```bash
    export FLASK_APP=app.py
    flask run --host=0.0.0.0 --port=5000

6. **Access the Application:**
    * Open your browser and go to`http://127.0.0.1:5000`.