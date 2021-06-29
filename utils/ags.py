import requests as r
import time
TOKEN = 'asdfasdfasdfasfd'


def post(url, body={}, reconnect_attempts=100, token=TOKEN):
    """sync fetcher for arcgis services"""
    body.update({
        "f": "json",
        "token": token
    })
    while reconnect_attempts:
        try:
            response = r.post(url, data=body, verify=False).json()
            if 'error' in response.keys():
                print(response)
            return response
        except ConnectionError:
            time.sleep(60)
            reconnect_attempts(-1)
            print('VPN disconnected')
        except Exception as e:
            print(e)


def post_async(url, body, check_interval=3, print_messages=False):
    """async fetcher for arcgis geoprocessing services"""
    submit_url = f"{url}/submitJob"
    job_id = post(submit_url, body)['jobId']
    print(f'Job id: {job_id}')
    finished = False
    messages = []
    new_messages = []
    job_response = None
    while not finished:
        time.sleep(check_interval)
        job_status_url = f"{url}/jobs/{job_id}"
        job_response = post(job_status_url)
        job_status = job_response["jobStatus"]

        if job_status in ["esriJobFailed", "esriJobSucceeded"]:
            # print(f'Job status: {job_response["jobStatus"]}')
            if job_status == "esriJobFailed":
                print(f"Job failed: {job_id}")

            finished = True

        if print_messages:
            res_messages = [m['description']
                            for m in job_response['messages'] if m['description']]
            new_messages_count = len(messages) - len(res_messages)
            if new_messages_count:
                new_messages = res_messages[new_messages_count:]
                messages = res_messages

                for mess in new_messages:
                    print(f'\t{mess}')

    return job_response
