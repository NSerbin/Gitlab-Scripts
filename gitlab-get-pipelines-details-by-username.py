import requests
import json

def get_user_pipelines(project_id, username, token):
    # Get user ID based on the username
    user_url = f"https://gitlab.com/api/v4/users?username={username}"
    headers = {"PRIVATE-TOKEN": token}
    user_response = requests.get(user_url, headers=headers)

    output_data = {"pipelines": []}

    if user_response.status_code == 200:
        user_data = user_response.json()

        if not user_data:
            output_data["error"] = f"User with username {username} not found."
        else:
            user_id = user_data[0]["id"]

            # Get all pipelines for the user
            user_pipelines_url = f"https://gitlab.com/api/v4/projects/{project_id}/pipelines?user_id={user_id}"
            user_pipelines_response = requests.get(user_pipelines_url, headers=headers)

            if user_pipelines_response.status_code == 200:
                user_pipelines = user_pipelines_response.json()
                output_data["pipelines"] = user_pipelines
            else:
                output_data["error"] = f"Failed to retrieve pipelines for user with username {username}. Status code: {user_pipelines_response.status_code}"
    else:
        output_data["error"] = f"Failed to retrieve user information. Status code: {user_response.status_code}"

    # Convert the output_data to JSON and print it
    print(json.dumps(output_data, indent=2))

# Replace these variables with your own values
project_id = "CHANGE-ME"
username = "CHANGE-ME"  # Replace with the actual username
token = "CHANGE-ME"

get_user_pipelines(project_id, username, token)