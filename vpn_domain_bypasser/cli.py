import json
import pathlib
from pprint import pprint
import traceback


def make_and_get_directory_path():
    directory_path = pathlib.Path("vpn_domain_bypasser_config")
    directory_path.mkdir(exist_ok=True, parents=True)
    return directory_path


def get_config_file_path():
    directory_path = make_and_get_directory_path()
    return directory_path / "config.json"


def save_config(config_dict: dict):
    """Does not utilize global var"""

    file_path = get_config_file_path()

    with open(str(file_path), "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=4)


def load_config() -> dict:
    """Does not utilize global var"""

    config_dict = {
        "domains": [],
        "gateway": "",
        "polling_interval": 60,
    }

    file_path = get_config_file_path()
    if not file_path.exists():
        return config_dict

    try:
        with open(str(file_path), "r", encoding="utf-8") as f:
            config_dict = json.load(f)
    except:
        traceback.print_exc()

    return config_dict


def main():
    global config_dict
    from globals import config_dict

    print("Current config:")
    pprint(config_dict)

    for key in config_dict:
        if key == "domains":
            while True:
                add = input(f"Would you like to add a domain name? (Y or N): ")
                add = add.strip().upper()
                if add == "Y":
                    domain = input(f"Enter a domain: ")
                    if domain and domain.strip():
                        config_dict[key].append(domain.strip())
                else:
                    break

            if config_dict[key]:
                delete_any = input(
                    f"Would you like to delete a domain name? (Y or N): "
                )
                delete_any = delete_any.strip().upper()
                if delete_any == "Y":
                    to_delete_list = []
                    for domain in config_dict[key]:
                        delete = input(f"Delete {domain}? (Y or N): ")
                        delete = delete.strip().upper()
                        if delete == "Y":
                            to_delete_list.append(domain.lower().strip())

                    if to_delete_list:
                        config_dict[key] = [
                            domain
                            for domain in config_dict[key]
                            if domain.lower().strip() not in to_delete_list
                        ]

        else:
            original_value = config_dict[key]
            if original_value and str(original_value).strip():
                value = input(f"Enter new value for {key} ({original_value}): ")
            else:
                value = input(f"Enter new value for {key}: ")

            if value and value.strip():
                if key == "polling_interval":
                    config_dict[key] = int(value.strip())
                else:
                    config_dict[key] = value.strip()

    print("Current config:")
    pprint(config_dict)

    save_config(config_dict)


if __name__ == "__main__":
    main()
