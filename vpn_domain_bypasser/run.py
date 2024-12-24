import time

from globals import domain_to_ip_dict
from route import add_route, delete_route
from socket_utils import get_ip_for_domain

from cli import main as cli_main
from globals import config_dict


def process_all_domains():
    global config_dict, domain_to_ip_dict

    for domain in config_dict["domains"]:
        new_ip = get_ip_for_domain(domain)

        if new_ip:
            current_ip = domain_to_ip_dict.get(domain)

            # if IP has changed, update the routing table
            if new_ip != current_ip:
                # don't delete as IPs are constantly changing, so this will accumulate most after some time
                # just reboot system to clear all entries since these are not persistent routes
                # if current_ip:
                #    delete_route(current_ip)

                add_route(new_ip, config_dict["gateway"])
                domain_to_ip_dict[domain] = new_ip


def is_config_setup():
    global config_dict

    return (
        config_dict["domains"]
        and config_dict["gateway"].strip()
        and str(config_dict["polling_interval"]).strip()
    )


def main():
    global config_dict

    if not is_config_setup():
        print("Config not setup up. This is required. Redirecting to enter...")
        cli_main()

    if not is_config_setup():
        print("Config still not set up. Exiting program...")
        return

    while True:
        process_all_domains()
        time.sleep(config_dict["polling_interval"])


if __name__ == "__main__":
    main()
