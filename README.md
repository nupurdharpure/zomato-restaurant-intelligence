# 🍽️ Zomato Restaurant Intelligence Dashboard

An interactive data analytics web app analysing 6,500+ restaurant listings 
across India — built to uncover business insights for food-tech decision making.

## 🔗 Live App
[Click here to open the live dashboard](https://zomato-restaurant-intelligence-ad4fxux2tsstokygvxscds.streamlit.app)

## 📊 What This App Does
- Analyses restaurant distribution across Indian cities
- Compares cuisines by rating, cost and popularity
- Answers: does spending more actually get you better food?
- Identifies overrated restaurants (high votes, low rating)
- Interactive filters for city, cuisine and price range
- Built with real-world Zomato data (9,500+ listings across 15 countries, filtered to 6,500+ Indian restaurants)

## 💡 Key Insights Found
- 62% of all Indian Zomato restaurants are in Delhi NCR
- Luxury restaurants rate 16% higher than budget ones
- North Indian cuisine is the most oversaturated market in Delhi
- Online delivery has almost no impact on restaurant quality

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Data cleaning and analysis |
| Pandas | Data manipulation |
| MySQL | SQL querying and analysis |
| Matplotlib / Seaborn | Data visualisation |
| Streamlit | Interactive web app |
| Git / GitHub | Version control |

## 📁 Project Structure
zomato_project/
├── app.py              # Streamlit web app
├── charts.ipynb        # Python charts notebook
├── analysis.sql        # All SQL queries
├── requirements.txt    # Python dependencies
└── zomato_clean.csv    # Cleaned dataset

## 🚀 Run Locally
```bash
git clone https://github.com/nupurdharpure/zomato-restaurant-intelligence
cd zomato-restaurant-intelligence
pip install -r requirements.txt
streamlit run app.py
```

## 👩‍💻 Author
**Nupur Dharpure** — Data Science fresher | Pune, India  
[LinkedIn](https://www.linkedin.com/in/nupur-dharpure-0179bb266/) | [GitHub](https://github.com/nupurdharpure)