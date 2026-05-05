from bs4 import BeautifulSoup


def get_tokens(soup):
    def safe_get(id_):
        el = soup.find(id=id_)
        return el["value"] if el else None

    return {
        "__VIEWSTATE": safe_get("__VIEWSTATE"),
        "__EVENTVALIDATION": safe_get("__EVENTVALIDATION"),
        "__VIEWSTATEGENERATOR": safe_get("__VIEWSTATEGENERATOR"),
    }

def parse_quota(soup: BeautifulSoup) -> str:
    el = soup.find(id="ctl00_bodyPH_lblquota")
    return el.text.strip() if el else ""


def extract_options(soup, select_id):
    select = soup.find(id=select_id)
    if not select:
        return []

    options = []
    for opt in select.find_all("option"):
        value = opt.get("value", "").strip()
        text = opt.text.strip().lower()

        # skip invalid/default options
        if not value or value == "0" or "select" in text:
            continue

        options.append(value)

    return options