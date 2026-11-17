from flask import Flask, request, render_template

from ip_checker.validator import check_ip_format, get_ip_version
from ip_checker.database import (
    create_table,
    insert_ip,
    record_activity,
    get_activity_history,
    get_dashboard_stats
)

app = Flask(__name__)

# Make sure both database tables exist
create_table()


def process_ip(ip):
    cleaned_ip = check_ip_format(ip)

    if cleaned_ip == "Invalid IP format":
        record_activity(ip, "Invalid", "N/A")
        return "Invalid IP format"

    version = get_ip_version(cleaned_ip)
    version_name = f"IPv{version}"

    # Save the valid IP in the unique IP records table
    insert_ip(cleaned_ip)

    # Save every checking attempt in activity history
    record_activity(cleaned_ip, "Valid", version_name)

    return (
        f"IP: {cleaned_ip} is a valid IP address. "
        f"Version: {version_name}"
    )


@app.route("/")
def hello():
    ip = request.args.get("ip", "").strip()
    result = None

    if ip:
        result = process_ip(ip)

    selected_filter = request.args.get("filter", "All")

    if selected_filter not in ("All", "Valid", "Invalid"):
        selected_filter = "All"

    if selected_filter == "All":
        history = get_activity_history()
    else:
        history = get_activity_history(selected_filter)

    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        result=result,
        entered_ip=ip,
        history=history,
        stats=stats,
        selected_filter=selected_filter
    )


@app.route("/check")
def check():
    ip = request.args.get("ip", "").strip()

    if not ip:
        return "No IP provided. Please provide an IP address to check."

    return process_ip(ip)


if __name__ == "__main__":
    app.run(debug=True)