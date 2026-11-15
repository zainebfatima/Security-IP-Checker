from pathlib import Path
import json
import csv

DATA_FILE = Path(__file__).resolve().parent.parent / "ip_records.json"

def save_records(ips, flagged_ips):
    data = {
        "ips": ips,
        "flagged_ips": flagged_ips
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_records():
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        return data.get("ips", []), data.get("flagged_ips", [])

def export_to_csv(ips, flagged_ips):
     with open("ip_records.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Flagged"])
        for ip in ips:
            flagged = "Yes" if ip in flagged_ips else "No"
            writer.writerow([ip, flagged])