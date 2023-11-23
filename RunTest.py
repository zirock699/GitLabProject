import argparse
import json

import requests
import xml.etree.ElementTree as ET

def RunTest(post_run_action, test_id, test_instance_id, hours, minutes, vuds_mode, LWSSO_COOKIE_KEY):
    url = "http://nimbuswindows.aos.com/LoadTest/rest/domains/DEFAULT/projects/AOS_Nimbus/Runs"
    headers = {
        "Content-Type": "application/xml",
        "Cookie": f"LWSSO_COOKIE_KEY={LWSSO_COOKIE_KEY}"
    }
    body = f"""
        <Run xmlns="http://www.hp.com/PC/REST/API">
          <PostRunAction>{post_run_action}</PostRunAction>
          <TestID>{test_id}</TestID>
          <TestInstanceID>{test_instance_id}</TestInstanceID>
          <TimeslotDuration>
            <Hours>{hours}</Hours>
            <Minutes>{minutes}</Minutes>
          </TimeslotDuration>
          <VudsMode>{str(vuds_mode).lower()}</VudsMode>
        </Run>
        """
    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = "{http://www.hp.com/PC/REST/API}"
        status_Code = response.status_code
        return json.dumps({"StatusCode": response.status_code, "RunId": root.find(f'{ns}ID').text})
    except requests.RequestException as e:
        return f"Error in request: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Test Script.')
    parser.add_argument('-postrunaction', type=str, default='Collate And Analyze')
    parser.add_argument('-testid', type=str, default='177')
    parser.add_argument('-testinstanceid', type=str, default='8')
    parser.add_argument('-hours', type=int, default=1)
    parser.add_argument('-minutes', type=int, default=30)
    parser.add_argument('-vudsmode', type=str, default='false')
    parser.add_argument('-LWSSO_COOKIE_KEY',type=str,default='IFdzNFM09vmSNtS9WVz2H9NtUE9-JmTyGCnqdqroQcYtz1vFKIbplE2DA4ny6WEOm162hXbA7FI6oh6nEsARTe0rHBRk6yGfTRob_C4yQKXxI4IbXpNfg0du0_RvVv4J2UfxpxmQmM_hshGiKkOJGGOWijz94-FlK1dZ0MZYw06MDvCfMkvsDfCiG0luEJubGTHDBylc7IuJlEXk-2JTdVOh-BA741WjYdL5AUr0t84.')
    args = parser.parse_args()
    print(RunTest(args.postrunaction, args.testid, args.testinstanceid, args.hours, args.minutes, args.vudsmode,args.LWSSO_COOKIE_KEY))