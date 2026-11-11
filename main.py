from ip_checker.validator import is_valid_ip, get_ip_version

def main():
    ip = input("Enter an IP address: ")
    if is_valid_ip(ip):
        version = get_ip_version(ip)
        print(f"{ip} is a valid IP address.")
        print(f"IP version: {version}")
    else:
        print(f"{ip} is not a valid IP address.")

main()
