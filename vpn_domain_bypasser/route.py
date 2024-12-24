import subprocess
import traceback


def add_route(ip, gateway):
    try:
        print(f"Adding route for {ip} via {gateway}")
        subprocess.run(["route", "add", ip, gateway, "metric", "1"], check=True)
    except:
        traceback.print_exc()


def delete_route(ip):
    try:
        print(f"Deleting route for {ip}")
        subprocess.run(["route", "delete", ip], check=True)
    except:
        traceback.print_exc()
