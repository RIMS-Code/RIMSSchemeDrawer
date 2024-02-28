import json

from iniabu import ini
import requests


def get_url(ele: str) -> str:
    """Get URL for csv file from NIST.

    :param ele: String of element, e.g., Mg

    :return: URL to get csv file from NIST.
    """
    url = (
        f"https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum={ele}+"
        f"I&units=0&format=2&output=0&page_size=15&multiplet_ordered=0&conf_out"
        f"=on&term_out=on&level_out=on&unc_out=1&j_out=on&lande_out=on&perc_out"
        f"=on&biblio=on&temp=&submit=Retrieve+Data"
    )
    return url


def get_ip(ele: str) -> float:
    """Get ionization potential from NIST.

    :param ele: String of element, e.g., Mg

    :return: Ionization potential in eV.
    """
    data = requests.get(get_url(ele)).text
    data = data.split("\n")

    # find limit line in data
    for it, line in enumerate(data):
        if "Limit" in line:
            idx = it
            break

    line = data[idx].replace('"', "").replace("=", "").split(",")
    # print(line)
    ip = line[4]
    if ip == "[" or ip == "":
        ip = line[5]  # we got a best guess value in []
    return float(ip)


elements = ini.ele_dict.keys()  # list of all elements
ele_ips = {}

# print(elements)

# print(get_ip("Tb"))

for ele in elements:
    print(f"{ele} is up")
    ele_ips[ele] = get_ip(ele)

with open("ip_nist.json", "w") as fout:
    json.dump(ele_ips, fout, indent=4)
