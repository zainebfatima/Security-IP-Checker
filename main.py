from ip_checker.validator import  get_ip_version, check_ip_format

def main():
    ip = input("Enter an IP address: ")
    result = check_ip_format(ip)
    if result == "Empty input":
        print("You entered an empty input. Please provide a valid IP address.")
    elif result == "Invalid IP format":
        print("The IP address format is invalid. Please provide a valid IP address.")
    else:
        ip = result
        version = get_ip_version(ip)

        print(f"{ip} is a valid IP address.")
        print(f"IP version: IPv{version}")

main()
