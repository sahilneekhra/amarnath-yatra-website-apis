from fastapi import FastAPI, Query
from datetime import date, timedelta

from client import AmarnathClient
from parser import extract_options

app = FastAPI(
    title="Amarnath Yatra Availability API",
    description="""
Check Amarnath Yatra slot availability between a date range.

- Supports routes like **Baltal** and **Pahalgam**
- Dates not present in official dropdown → marked as **Yatra Closed**
- Returns available slots if present

⚠️ Note: Data is fetched live from official website (may be slow)
""",
    version="1.0.0"
)


def format_date_for_site(dt: date) -> str:
    return dt.strftime("%d %B %Y")  # required by website


def format_date_for_output(dt: date) -> str:
    return dt.strftime("%d/%m/%Y")  # user-friendly


def generate_date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


@app.get("/test")
def test(start: date, end: date):
    return {"start": start, "end": end}

@app.get(
    "/availability",
    summary="Check slot availability for date range",
    description="Returns slot availability for given route and date range"
)
def get_availability(
    route: str = Query(
        ...,
        description="Route name (e.g., Baltal, Pahalgam)"
    ),
    start: date = Query(
        ...,
        description="Start date (select from calendar)"
    ),
    end: date = Query(
        ...,
        description="End date (select from calendar)"
    )
):
    client = AmarnathClient()
    client.load()

    available_dates = extract_options(client.soup, "ctl00_bodyPH_ydate")
    routes = extract_options(client.soup, "ctl00_bodyPH_ddlroute")

    if route not in routes:
        return {"error": f"Invalid route. Available: {routes}"}

    results = []

    for dt in generate_date_range(start, end):
        site_format = format_date_for_site(dt)
        output_format = format_date_for_output(dt)

        # If date not in dropdown → closed
        if site_format not in available_dates:
            results.append({
                "route": route,
                "date": output_format,
                "status": "Yatra Closed"
            })
            continue

        try:
            result = client.check(route, site_format)

            results.append({
                "route": route,
                "date": output_format,
                "quota": result.quota_text,
                "slots": result.slots
            })

        except Exception as e:
            results.append({
                "route": route,
                "date": output_format,
                "status": f"Error: {str(e)}"
            })

    return {
        "route": route,
        "start": start.strftime("%d/%m/%Y"),
        "end": end.strftime("%d/%m/%Y"),
        "results": results
    }