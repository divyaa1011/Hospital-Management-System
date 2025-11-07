"""Minimal CLI to call the API."""

import requests
from pprint import pprint

BASE = "http://127.0.0.1:5000"

def list_patients():
    r = requests.get(f"{BASE}/patients")
    r.raise_for_status()
    data = r.json()
    if not data:
        print("No patients.")
        return
    for p in data:
        pprint(p)

def add_patient():
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    disease = input("Disease: ").strip()
    payload = {"name": name, "age": age, "disease": disease}
    r = requests.post(f"{BASE}/patients", json=payload)
    if r.status_code == 201:
        print("Created:", r.json())
    else:
        print("Error:", r.status_code, r.text)

def avg_age():
    r = requests.get(f"{BASE}/patients/average-age")
    print(r.json())

def scrape():
    url = input("URL to scrape (enter for WHO): ").strip()
    if not url:
        url = "https://www.who.int"
    r = requests.get(f"{BASE}/scrape", params={"url": url})
    print(r.json())

def menu():
    print("\nHMS CLI\n1.List\n2.Add\n3.Average age\n4.Scrape\n5.Exit")
    return input("Choice: ").strip()

def main():
    while True:
        c = menu()
        if c == "1":
            list_patients()
        elif c == "2":
            add_patient()
        elif c == "3":
            avg_age()
        elif c == "4":
            scrape()
        elif c == "5":
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()
