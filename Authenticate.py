import requests
import argparse
import json

def Authenticate(ClientIdKey, ClientSecretKey):
    url = "http://nimbuswindows.aos.com/LoadTest/rest/authentication-point/AuthenticateClient"
    payload = json.dumps({
        "ClientIdKey": f"{ClientIdKey}",
        "ClientSecretKey": f"{ClientSecretKey}"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    LWSSO_COOKIE_KEY=str(response.cookies.values()[0])
    status_Code = response.status_code
    return json.dumps({"StatusCode": response.status_code, "LWSSO_COOKIE_KEY": LWSSO_COOKIE_KEY})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Authenticate app.')
    parser.add_argument('-ClientIdKey', type=str, default='I_KEY_74cd7d5d-cec6-4f30-8e41-29d5b8bbd2b5')
    parser.add_argument('-ClientSecretKey', type=str, default='S_KEY_f240c524-d2b4-4cf9-991a-3394a5ec4a53')
    args = parser.parse_args()
    print(Authenticate(args.ClientIdKey, args.ClientSecretKey))