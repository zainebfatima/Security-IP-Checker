import ipaddress

from ip_checker.storage import load_records, save_records, export_to_csv


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def get_ip_version(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.version
    except ValueError:
        return None


def check_ip_format(ip):
    ip = ip.strip()
    if not ip:
        return "Empty input"
    if not is_valid_ip(ip):
        return "Invalid IP format"
    return ip


def find_duplicate_ips(ips):
    seen_ips = set()
    duplicates = set()
    for ip in ips:
        if ip in seen_ips:
            duplicates.add(ip)
        else:
            seen_ips.add(ip)
    return list(duplicates)


def add_ip(ips, new_ip):
    if new_ip not in ips:
        ips.append(new_ip)
        return True
    return False


def flag_ip(ips, flagged_ips, ip):
    if ip not in ips:
        return "IP not found in records."
    if ip in flagged_ips:
        return "IP already flagged."

    flagged_ips.append(ip)
    return "IP successfully flagged."


if __name__ == "__main__":
    ips, flagged_ips = load_records()

    while True:
        print("\n1. Add IP")
        print("2. Flag IP")
        print("q. Quit")

        choice = input("Choose an option: ").strip()

        # Exit
        if choice.lower() == "q":
            break

        # Add IP
        if choice == "1":
            new_ip = input("Enter an IP address: ").strip()

            # Check empty input
            if not new_ip:
                print("Empty input! Please enter an IP.")
                continue

            # Check IP format
            checked_ip = check_ip_format(new_ip)

            if checked_ip in ("Empty input", "Invalid IP format"):
                print(checked_ip)
                print("IP rejected!")
                continue

            # Validate IP
            if is_valid_ip(checked_ip):
                print("Valid IP!")

            # Identify IP version
            version = get_ip_version(checked_ip)
            print(f"IP Version: IPv{version}")

            # Check duplicates
            if checked_ip in ips:
                print("Duplicate IP! Already exists.")
                continue

            # Add IP
            result = add_ip(ips, checked_ip)

            if result:
                print("IP successfully added!")
                save_records(ips, flagged_ips)
                export_to_csv(ips, flagged_ips)

            print("IP Records:", ips)

        # Flag IP
        elif choice == "2":
            ip_to_flag = input("Enter an IP address to flag: ").strip()

            # Check empty input
            if not ip_to_flag:
                print("Empty input! Please enter an IP.")
                continue

            # Check IP format
            checked_ip = check_ip_format(ip_to_flag)

            if checked_ip in ("Empty input", "Invalid IP format"):
                print(checked_ip)
                print("IP rejected!")
                continue

            # Flag IP
            result = flag_ip(ips, flagged_ips, checked_ip)

            print(result)

            if result == "IP successfully flagged.":
                save_records(ips, flagged_ips)
                export_to_csv(ips, flagged_ips)
                print("IP Records:", ips)
            print("Flagged IPs:", flagged_ips)

        else:
            print("Invalid choice! Please choose 1, 2, or q.")

    print("\nFinal IP Records:", ips)
    print("Final Flagged IPs:", flagged_ips)