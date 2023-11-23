import argparse
import time
import requests
import xml.etree.ElementTree as ET

class RunStatus:
    def __init__(self, test_id, test_instance_id, post_run_action, timeslot_id, vuds_mode, run_id, duration, run_state, run_sla_status=""):
        self.test_id = test_id
        self.test_instance_id = test_instance_id
        self.post_run_action = post_run_action
        self.timeslot_id = timeslot_id
        self.vuds_mode = vuds_mode
        self.run_id = run_id
        self.duration = duration
        self.run_state = run_state
        self.run_sla_status = run_sla_status

    def __str__(self):
        return (f"RunStatus(TestID={self.test_id}, TestInstanceID={self.test_instance_id}, "
                f"PostRunAction={self.post_run_action}, TimeslotID={self.timeslot_id}, "
                f"VudsMode={self.vuds_mode}, ID={self.run_id}, Duration={self.duration}, "
                f"RunState={self.run_state}, RunSLAStatus={self.run_sla_status})")
    # Getters
    def get_test_id(self):
        return self.test_id

    def get_test_instance_id(self):
        return self.test_instance_id

    def get_post_run_action(self):
        return self.post_run_action

    def get_timeslot_id(self):
        return self.timeslot_id

    def get_vuds_mode(self):
        return self.vuds_mode

    def get_run_id(self):
        return self.run_id

    def get_duration(self):
        return self.duration

    def get_run_state(self):
        return self.run_state

    def get_run_sla_status(self):
        return self.run_sla_status

    # Setters
    def set_test_id(self, test_id):
        self.test_id = test_id

    def set_test_instance_id(self, test_instance_id):
        self.test_instance_id = test_instance_id

    def set_post_run_action(self, post_run_action):
        self.post_run_action = post_run_action

    def set_timeslot_id(self, timeslot_id):
        self.timeslot_id = timeslot_id

    def set_vuds_mode(self, vuds_mode):
        self.vuds_mode = vuds_mode

    def set_run_id(self, run_id):
        self.run_id = run_id

    def set_duration(self, duration):
        self.duration = duration

    def set_run_state(self, run_state):
        self.run_state = run_state

    def set_run_sla_status(self, run_sla_status):
        self.run_sla_status = run_sla_status
def CheckRunStatus(RunId, LWSSO_COOKIE_KEY):
    url = "http://nimbuswindows.aos.com/LoadTest/rest/domains/DEFAULT/projects/AOS_Nimbus/Runs/"+str(RunId)
    headers = {
        "Cookie": f"LWSSO_COOKIE_KEY={LWSSO_COOKIE_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Parse XML response content
        root = ET.fromstring(response.content)
        ns = "{http://www.hp.com/PC/REST/API}"
        run_status = RunStatus(
            test_id=root.find(f'{ns}TestID').text,
            test_instance_id=root.find(f'{ns}TestInstanceID').text,
            post_run_action=root.find(f'{ns}PostRunAction').text,
            timeslot_id=root.find(f'{ns}TimeslotID').text,
            vuds_mode=root.find(f'{ns}VudsMode').text,
            run_id=root.find(f'{ns}ID').text,
            duration=root.find(f'{ns}Duration').text,
            run_state=root.find(f'{ns}RunState').text,
            run_sla_status=root.find(f'{ns}RunSLAStatus').text
        )
        return run_status
    except requests.RequestException as e:
        return f"Error in request: {e}"


def monitor_run_status(run_id, wait_seconds, max_attempts, LWSSO_COOKIE_KEY):
    attempts = 0
    while attempts < max_attempts:
        run_status = CheckRunStatus(run_id, LWSSO_COOKIE_KEY)
        # Check if the function returned an error message
        if isinstance(run_status, str):
            return run_status
        if run_status.get_run_state() == "Finished":
            return ('Finished')
        # Wait for the specified number of seconds before the next check
        time.sleep(wait_seconds)
        attempts += 1
    return "Maximum number of attempts reached."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor Run Status')
    parser.add_argument('-run_id', type=str, default='82')
    parser.add_argument('-wait_seconds', type=int, default=10)
    parser.add_argument('-max_attempts', type=int, default=200)
    parser.add_argument('-LWSSO_COOKIE_KEY',type=str,default='IFdzNFM09vmSNtS9WVz2H9NtUE9-JmTyGCnqdqroQcYtz1vFKIbplE2DA4ny6WEOm162hXbA7FI6oh6nEsARTe0rHBRk6yGfTRob_C4yQKXxI4IbXpNfg0du0_RvVv4J2UfxpxmQmM_hshGiKkOJGGOWijz94-FlK1dZ0MZYw06MDvCfMkvsDfCiG0luEJubGTHDBylc7IuJlEXk-2JTdVOh-BA741WjYdL5AUr0t84.')
    args = parser.parse_args()
    print(monitor_run_status(args.run_id, args.wait_seconds, args.max_attempts, args.LWSSO_COOKIE_KEY))