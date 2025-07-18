import requests
import csv
from datetime import datetime


ACCESS_TOKEN = "your_access_token_here"
ENTITY_ID = 1620  # AIESEC in Sri Lanka 
START_DATE = "2024-02-14"
END_DATE = "2024-07-31"
CSV_FILENAME = "igv_approvals_realizations_srilanka.csv"


headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def fetch_igv_data(page=1):
    url = f"https://gis-api.aiesec.org/v2/applications"
    params = {
        "page": page,
        "per_page": 100,
        "opportunity_programmes[]": 1,  # 1 = GV
        "opportunity_committee_id": ENTITY_ID,
        "updated_after": START_DATE,
        "updated_before": END_DATE,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def main():
    approvals = 0
    realizations = 0
    page = 1
    applications = []

    while True:
        data = fetch_igv_data(page)
        if not data or len(data['data']) == 0:
            break

        for app in data['data']:
            status = app['status']
            updated_at = app['updated_at'][:10]  # format: YYYY-MM-DD
            if START_DATE <= updated_at <= END_DATE:
                if status == "approved":
                    approvals += 1
                elif status == "realized":
                    realizations += 1

                applications.append({
                    "Opportunity ID": app['opportunity']['id'],
                    "EP Name": app['person']['full_name'],
                    "Status": status,
                    "Updated At": updated_at
                })

        page += 1


    with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Opportunity ID", "EP Name", "Status", "Updated At"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in applications:
            writer.writerow(row)

    print(f"Export complete! Approvals: {approvals}, Realizations: {realizations}")
    print(f"File saved as: {CSV_FILENAME}")


if __name__ == "__main__":
    main()















