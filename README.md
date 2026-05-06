# Amarnath_Yatra_Website_APIs

## ⚠️ Disclaimer

This project is an **unofficial, personal project** and is **not affiliated with, endorsed by, or connected to the Shri Amarnath Shrine Board**.

It accesses publicly available data from the official website and is intended **strictly for educational use**.

- This is **not an official API**
- Do not rely on it for critical decisions
- Please avoid excessive automated requests that may impact the source website

The developer is not responsible for any misuse or inaccuracies in the data.

---

A FastAPI-based service that checks **live slot availability** for the Amarnath Yatra by reverse-engineering the official website.

Instead of manually selecting dates one by one, this API allows you to query availability across a **date range** programmatically.

---
## 🚀 Live API

👉 https://amarnath-yatra-website-apis.onrender.com/docs

### Example

GET https://amarnath-yatra-website-apis.onrender.com/availability?route=Baltal&start=2026-08-04&end=2026-08-14
---

## ✨ Features

* 🔍 Check availability for **Baltal / Pahalgam routes**
* 📅 Query **date ranges instead of single dates**
* ⚡ Automatically detects:

  * Available slots (e.g., `1983 left`)
  * Closed dates → `Yatra Closed`
* 🧠 Handles ASP.NET WebForms internally (VIEWSTATE, EVENTTARGET, etc.)
* 📊 Structured JSON response
* 📘 Interactive API docs via Swagger

---

## 🧱 Tech Stack

* **Backend:** FastAPI
* **HTTP Client:** requests
* **Parsing:** BeautifulSoup
* **Server:** Uvicorn

---

## 📦 Installation

```bash
git clone https://github.com/your-username/Amarnath_Yatra_Website_APIs.git
cd Amarnath_Yatra_Website_APIs

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
python -m uvicorn api:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Usage

### Endpoint

```
GET /availability
```

### Query Parameters

| Parameter | Type   | Description                         |
| --------- | ------ | ----------------------------------- |
| route     | string | Route name (`Baltal` or `Pahalgam`) |
| start     | date   | Start date (format: `YYYY-MM-DD`)   |
| end       | date   | End date (format: `YYYY-MM-DD`)     |

---

### 🔥 Example Request

```
GET /availability?route=Baltal&start=2026-07-10&end=2026-07-15
```

---

### ✅ Example Response

```json
{
  "route": "Baltal",
  "start": "10/07/2026",
  "end": "15/07/2026",
  "results": [
    {
      "route": "Baltal",
      "date": "10/07/2026",
      "quota": "1200 left",
      "slots": 1200
    },
    {
      "route": "Baltal",
      "date": "11/07/2026",
      "status": "Yatra Closed"
    }
  ]
}
```

---

## 🧠 How It Works

This project **does not use an official API** (none exists).

Instead, it:

1. Loads the official Amarnath website
2. Extracts hidden ASP.NET tokens:

   * `__VIEWSTATE`
   * `__EVENTVALIDATION`
3. Simulates form submission (`__EVENTTARGET`)
4. Parses the returned HTML response
5. Converts it into structured JSON

---

## ⚠️ Important Notes

* ⏳ API may be slow (depends on official site response)
* 🚫 Excessive usage may get IP blocked
* 🌐 Data is fetched live — accuracy depends on source site
* 📅 Input date format must be: `YYYY-MM-DD`

---

## 📁 Project Structure

```
amarnath_api/
│
├── api.py        # FastAPI endpoints
├── client.py     # Request + session handling
├── parser.py     # HTML parsing logic
├── models.py     # Data structures
├── utils.py      # Helper functions
├── main.py       # CLI runner (optional)
└── requirements.txt
```

---

## 🚀 Deployment

Recommended platforms:

* Render (easy & free)
* Railway
* Fly.io

Start command:

```bash
uvicorn api:app --host 0.0.0.0 --port 10000
```

---

## 🔮 Future Improvements

* ⚡ Caching (Redis) to improve speed
* 🔔 Slot availability alerts
* 📊 Dashboard (Streamlit UI)
* 🔁 Parallel requests for faster responses

---

## 🤝 Contributing

Feel free to fork, improve, and raise PRs.

---

## 📜 License

MIT License

---

## 🙏 Disclaimer

This project is for **educational purposes only**.
It uses publicly available data from the official Amarnath website.
Please use responsibly and avoid excessive load on the source system.
