# py modules
import requests
import json

HEADERS = {"Content-Type": "application/json",
           "Accept": "vdn.dac.v1"}

def get_moxa_value(ip, data_addr):
    """
    Read value from moxa device 

    Args:
        ip (str): ip address of the moxa device
        data_addr (str): name of the data to read

    Returns:
        dict: value read form device, if reading fails None
    """
    try:
        resp = requests.get(
            "http://" + ip + "/api/slot/0/io/" + data_addr,
            headers = HEADERS)
        if not (resp.ok):
            print("ERROR not ok web page")
            return None
        resp = resp.json()
    except OSError:
        print("ERROR failed connection to ip: " + ip)
        return None
    except json.decoder.JSONDecodeError:
        print("ERROR with JSON parsing")
        return None
    return resp


def set_moxa_value(ip, data_addr, value):
    """
    Write value to moxa device 

    Args:
        ip (str): ip address of the moxa device
        data_addr (str): name of the data to write
        value(dict): value to be read

    Returns:
        bool: True if write successed, False if write failed
    """
    headers = HEADERS
    headers["Content-Length"] = str(len(value))
    try:
        resp_put = requests.put(
            "http://" + ip + "/api/slot/0/io/" + data_addr,
            headers = headers,
            json = value)
        if not resp_put.ok:
            print("ERROR not ok put web page")
            return False
        return True
    except OSError:
        print("ERROR failed connection to ip: " + ip)
        return False
    except json.decoder.JSONDecodeError:
        print("ERROR with JSON parsing")
        return False
