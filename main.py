from client import AmarnathClient
from parser import extract_options
from utils import sleep


def main():
    client = AmarnathClient()
    client.load()
    # print(client.soup.prettify()[:2000])

    # selects = client.soup.find_all("select")
    # for s in selects:
    #     print(s.get("id"))

    # print("select id over")

    routes = extract_options(client.soup, "ctl00_bodyPH_ddlroute")
    dates = extract_options(client.soup, "ctl00_bodyPH_ydate")

    print(f"Found {len(routes)} routes and {len(dates)} dates\n")

    results = []

    for route in routes:
        for date in dates:
            try:
                result = client.check(route, date)
                results.append(result)

                print(
                    f"{result.route} | {result.date} | {result.quota_text}"
                )

                sleep(1)  # avoid hammering server

            except Exception as e:
                print(f"Error for {route} {date}: {e}")

    print("\n===== FINAL RESULTS =====\n")

    for r in results:
        print(r)


if __name__ == "__main__":
    main()