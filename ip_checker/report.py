from pathlib import Path
import ipaddress
from datetime import datetime

from ip_checker.storage import load_records
from ip_checker.validator import get_ip_version

REPORT_FILE = Path(__file__).resolve().parent.parent / "ip_report.txt"

def generate_report():
    ips, flagged_ips = load_records()
    report_lines = []
    report_lines.append(f"IP Records Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 50)
    all_ips = set(ips) | set(flagged_ips)
    report_lines.append(f"Total IPs: {len(all_ips)}")
    total_flagged = len(set(flagged_ips))
    total_unflagged = len(all_ips) - total_flagged

    ipv4_count = 0
    ipv6_count = 0

    report_lines.append(f"Flagged IPs: {total_flagged}")
    report_lines.append(f"Unflagged IPs: {total_unflagged}")
    report_lines.append("=" * 50)
    report_lines.append("IP Address\t\tVersion\t\tFlagged")
    report_lines.append("-" * 50)
    

    for ip in all_ips:
        version = get_ip_version(ip)
        if version == 4:
            ipv4_count += 1
        elif version == 6:
            ipv6_count += 1
        flagged = "Yes" if ip in flagged_ips else "No"
        report_lines.append(f"{ip:<20} IPv{version:<10} {flagged}")
    report_lines.append(f"IPv4 Addresses: {ipv4_count}")
    report_lines.append(f"IPv6 Addresses: {ipv6_count}")

    report_text = "\n".join(report_lines)

    with open(REPORT_FILE, "w") as file:
        file.write(report_text)

if __name__ == "__main__":
    generate_report()
    print("Report generated successfully!")