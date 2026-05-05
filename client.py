import requests
from bs4 import BeautifulSoup

from parser import get_tokens, parse_quota
from utils import extract_slots
from models import Availability


class AmarnathClient:
    BASE_URL = "https://jksasb.nic.in/onlineservices/register.aspx"

    def __init__(self):
        self.session = requests.Session()
        self.soup = None

    def load(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://jksasb.nic.in/",
            "Connection": "keep-alive"
        }

        res = self.session.get(self.BASE_URL, headers=headers)
        res.raise_for_status()

        self.soup = BeautifulSoup(res.text, "html.parser")

    def check(self, route: str, date: str):

        tokens = get_tokens(self.soup)

        if not tokens["__VIEWSTATE"]:
            raise Exception("VIEWSTATE missing - likely bad response or blocked")


        payload = {
            "__VIEWSTATE": tokens["__VIEWSTATE"],
            "__EVENTVALIDATION": tokens["__EVENTVALIDATION"],
            "__VIEWSTATEGENERATOR": tokens["__VIEWSTATEGENERATOR"],

            "__EVENTTARGET": "ctl00$bodyPH$Button1",
            "__EVENTARGUMENT": "",

            "ctl00$bodyPH$ddlroute": route,
            "ctl00$bodyPH$ydate": date,

            "ctl00$bodyPH$Button1": "Check Availability"
        }

        res = self.session.post(
            self.BASE_URL,
            data=payload,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": self.BASE_URL
            }
        )
        if "An Error Has Occurred" in res.text:
            raise Exception("Server returned error page")

        res.raise_for_status()

        self.soup = BeautifulSoup(res.text, "html.parser")

        quota_text = parse_quota(self.soup)
        slots = extract_slots(quota_text)

        return Availability(
            route=route,
            date=date,
            quota_text=quota_text,
            slots=slots
        )