import requests
from concurrent.futures import ThreadPoolExecutor

def delete_pipeline(pipeline_id, project_id, token):
    delete_url = f"https://gitlab.com/api/v4/projects/{project_id}/pipelines/{pipeline_id}"
    headers = {"PRIVATE-TOKEN": token}

    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        print(f"Pipeline {pipeline_id} deleted successfully.")
        return 1
    else:
        print(f"Failed to delete pipeline {pipeline_id}. Status code: {response.status_code}")
        return 0

def get_user_pipelines(project_id, user_id, token, page=1, per_page=20):
    user_pipelines_url = f"https://gitlab.com/api/v4/projects/{project_id}/pipelines?user_id={user_id}&page={page}&per_page={per_page}"
    headers = {"PRIVATE-TOKEN": token}

    response = requests.get(user_pipelines_url, headers=headers)

    if response.status_code == 200:
        user_pipelines = response.json()
        return user_pipelines
    else:
        print(f"Failed to retrieve pipelines for user. Status code: {response.status_code}")
        return []

def delete_user_pipelines(project_id, username, token):
    # Get user ID based on the username
    user_url = f"https://gitlab.com/api/v4/users?username={username}"
    headers = {"PRIVATE-TOKEN": token}
    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json()

        if not user_data:
            print(f"User with username {username} not found.")
            return

        user_id = user_data[0]["id"]

        # Use ThreadPoolExecutor for parallel deletion
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            page = 1
            deleted_count = 0

            while True:
                user_pipelines = get_user_pipelines(project_id, user_id, token, page=page)

                if not user_pipelines:
                    break

                for pipeline in user_pipelines:
                    futures.append(executor.submit(delete_pipeline, pipeline['id'], project_id, token))

                page += 1

            # Wait for all threads to finish and calculate the total deleted count
            for future in futures:
                deleted_count += future.result()

            print(f"Total pipelines deleted for user {username}: {deleted_count}")
    else:
        print(f"Failed to retrieve user information. Status code: {user_response.status_code}")

# Replace these variables with your own values
project_id = "CHANGE-ME"
username = "CHANGE-ME"  # Replace with the actual username
token = "CHANGE-ME"

delete_user_pipelines(project_id, username, token)