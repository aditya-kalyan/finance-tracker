import requests

BASE_URL = "http://localhost:8000"

def get_monthly_summary(token, year, month):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/reports/month", headers=headers, params={"year": year, "month": month})
    return res.json()

def get_yearly_summary(token, year):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/reports/year", headers=headers, params={"year": year})
    return res.json()

def get_by_month(token, year, month):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/by-month", headers=headers, params={"year": year, "month": month})
    return res.json()

def get_by_year(token, year):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/by-year", headers=headers, params={"year": year})
    return res.json()

def create_expense(token, data):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/expenses/create", headers=headers, json=data)
    return res.json()

def get_all_expenses(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/expenses/", headers=headers)
    return res.json()

def get_expense_by_id(token, expense_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/expenses/{expense_id}", headers=headers)
    return res.json()

def update_expense(token, expense_id, updated_data):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/expenses/{expense_id}", headers=headers, json=updated_data)
    return res.json()

def delete_expense(token, expense_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(f"{BASE_URL}/expenses/{expense_id}", headers=headers)
    return res.json()

def create_income(token, data):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/income/create", json=data, headers=headers)

    if res.status_code != 200:
        print("Failed Response:", res.status_code, res.text)
        res.raise_for_status()

    return res.json()

def get_all_income(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/income/", headers=headers)
    return res.json()

def download_excel_report(report_type, year, month=None):
    params = {"report_type": report_type, "year": year}
    if month:
        params["month"] = month
    res = requests.get(f"{BASE_URL}/reports/export", params=params)
    return res
