import ipaddress

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

ips = []

while True:
    new_ip = input("Enter an IP address (or 'q' to quit): ").strip()

    # Exit
    if new_ip.lower() == "q":
        break

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
    duplicates = find_duplicate_ips(ips)

    if checked_ip in ips:
        print("Duplicate IP! Already exists.")
        continue

    # Add IP
    result = add_ip(ips, checked_ip)

    if result:
        print("IP successfully added!")

    print("IP Records:", ips)

print("Final IP Records:", ips)
    