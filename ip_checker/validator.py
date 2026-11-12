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
    