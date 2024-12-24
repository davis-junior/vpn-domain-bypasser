import socket
import traceback


def get_ip_for_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        traceback.print_exc()
        return None
