import argparse
import requests
import xml.etree.ElementTree as ET

def CheckRunSLAStatusById(RunId, LWSSO_COOKIE_KEY):
    url = "http://nimbuswindows.aos.com/LoadTest/rest/domains/DEFAULT/projects/AOS_Nimbus/Runs/"+RunId

    headers = {
        "Cookie": f"LWSSO_COOKIE_KEY={LWSSO_COOKIE_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse XML response content
        root = ET.fromstring(response.content)
        ns = "{http://www.hp.com/PC/REST/API}"
        RunSLAStatus = root.find(f'{ns}RunSLAStatus').text
        return RunSLAStatus
    except requests.RequestException as e:
        return f"Error in request: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor Run Status')
    parser.add_argument('-run_id', type=str, default='91')
    parser.add_argument('-LWSSO_COOKIE_KEY',type=str,default='VUEHtdQYyW9xLU7Q-W6gml5BTPWFl3OYZw8_eUC1q0p4mnF26hPeevzaM_XeMnH1CeDmXRFojgtU9ollG-udzw2T9eRqhDJARJxdVu_cXMWjqOLcDqrz3rzbXzhSAn5gy1TbFlO5UqiYHAzDlQZ4t5cKNdXwQlXcLlFO-0k3Sq8z4cp-lxTulf4_8mEJEyI6IynrDqz_6W4qd-oFtJBFcBi4yrXWBMY_PSyae_G1GPY.')
    args = parser.parse_args()
    print(CheckRunSLAStatusById(args.run_id, args.LWSSO_COOKIE_KEY))