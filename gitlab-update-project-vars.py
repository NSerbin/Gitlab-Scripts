#!/usr/bin/env python3
import requests
import concurrent.futures

project_id = "CHANGE-ME"
token = "CHANGE-ME"
gitlab_url = f"https://gitlab.com/api/v4/projects/{project_id}/variables"
headers = {
    'PRIVATE-TOKEN': token,
    'Content-Type': 'application/json'
}

variable_type = ["env_var"] * 6
key = [
    "AWS_SG_ID",
    "AWS_SUBNET_1",
    "AWS_SUBNET_2",
    "AWS_SUBNET_3",
    "AWS_BUCKET_KMS_KEY",
    "AWS_LAMBDA_KMS_KEY"
]
value = [
    "AWS-SG-ID-VALUE",
    "AWS-SUBNET-1-VALUE",
    "AWS-SUBNET-2-VALUE",
    "AWS-SUBNET-3-VALUE",
    "AWS-BUCKET-KMS-KEY-VALUE",
    "AWS-LAMBDA-KMS-KEY-VALUE"
]
protected = ["false"] * 6
masked = ["true"] * 6
environment_scope = ["ENVIRONMENT-VALUE"] * 6

def create_variable(payload):
    session = requests.Session()
    response = session.post(gitlab_url, headers=headers, data=payload)
    session.close()
    return response

def gitlab_ci_variables():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for a, b, c, d, e, f in zip(variable_type, key, value, protected, masked, environment_scope):
            payload = json.dumps({
                "variable_type": a,
                "key": b,
                "value": c,
                "protected": d,
                "masked": e,
                "environment_scope": f,
            })
            future = executor.submit(create_variable, payload)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            print(response.text)

gitlab_ci_variables()
