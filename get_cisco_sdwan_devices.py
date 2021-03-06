#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Basic consumption of Cisco SD-WAN REST API using the
public Cisco DevNet sandbox.
"""

import requests
from requests.exceptions import HTTPError
from print_response import print_response


def main():
    """
    Execution begins here.
    """

    # Define base URL and disable SSL warnings (self-signed cert)
    api_path = "https://sandbox-sdwan-1.cisco.com"
    requests.packages.urllib3.disable_warnings()

    # These credentials are supplied by Cisco DevNet on the sandbox page:
    # https://developer.cisco.com/sdwan/learn/
    creds = {"j_username": "devnetuser", "j_password": "RG!_Yw919_83"}

    # Create session and issue POST request. "data" will unpack the dict
    # into key/value pairs. Also, disable SSL validation
    sess = requests.session()
    auth = sess.post(f"{api_path}/j_security_check", data=creds, verify=False)

    # Optional debugging statement
    # breakpoint()  # py3.7+
    # import pdb; pdb.set_trace()  # py3.6-

    # An authentication request has failed if we receive a failing return code
    # OR if there is any text supplied in the response. Failing authentications
    # often return code 200 (OK) but include a lot of HTML content, indicating a
    # a failure. If a failure does occur, exit the program using code 1.
    if not auth.ok or auth.text:
        raise HTTPError("Authentication failed")

    # Authentication succeeded; issue HTTP GET to collect devices
    devices = sess.get(f"{api_path}/dataservice/device", verify=False)
    devices.raise_for_status()
    print_response(devices, filename="get_cisco_sdwan_devices")


if __name__ == "__main__":
    main()
