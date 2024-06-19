import os
import requests
import json
import argparse
from tqdm import tqdm

##################################################
# COMMAND LINE ARGS
##################################################
parser = argparse.ArgumentParser(description='Rockset Org Metadata Script')
parser.add_argument('--apiKey', required=True, help='Rockset API key')
parser.add_argument('--debug', action='store_true', help='Enable debug mode for troubleshooting')
parser.add_argument('--verbose', action='store_true', help='Enable verbose mode for displaying exceptions')
parser.add_argument('--limit', type=int, default=None, help='Limit the number of collections processed')
args = parser.parse_args()

api_key = args.apiKey
verbose = args.verbose
collection_limit = args.limit

# Enable debug mode by default if collectionLimit is specified
debug_mode = args.debug or collection_limit is not None
##################################################

endpoints = [
    "users",
    "collections",
    "integrations",
    "lambdas",
    "aliases",
    "views",
    "ws"
]

def make_api_call(endpoint, api_key):
    url = f"https://api.usw2a1.rockset.com/v1/orgs/self/{endpoint}"
    headers = {
        'Authorization': f'ApiKey {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_collection_fields(workspace_name, collection_name, api_key, verbose):
    url = "https://api.usw2a1.rockset.com/v1/orgs/self/queries"
    query = f"DESCRIBE \"{workspace_name}\".\"{collection_name}\""
    payload = {
        "sql": {
            "query": query
        }
    }
    headers = {
        'Authorization': f'ApiKey {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("message", "")
        if "DESCRIBE is not supported on rollup collections" in error_message:
            if verbose:
                tqdm.write(f"Error describing {workspace_name}.{collection_name}: {e.response.text}")
            return []  # Return empty list of fields when a DESCRIBE for rollups occurs
        else:
            raise e
    result = response.json()
    return [{"name": field["field"][-1], "type": field["type"]} for field in result["results"]]

# Ensure the directory exists
os.makedirs("rockset_org", exist_ok=True)

with tqdm(total=len(endpoints), desc="Processing endpoints", ncols=80) as pbar:
    for endpoint in endpoints:
        tqdm.write(f"Processing endpoint: {endpoint}")
        try:
            data = make_api_call(endpoint, api_key)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Unauthorized access. Please check your API key.")
            else:
                raise e

        if debug_mode and endpoint == "collections":
            data["data"] = data["data"][:collection_limit]
        if endpoint == "collections":
            with tqdm(total=len(data["data"]), desc="Processing collections", ncols=80, leave=True, position=1) as col_pbar:
                for collection in data["data"]:
                    workspace_name = collection["workspace"]
                    collection_name = collection["name"]
                    collection["fields"] = get_collection_fields(workspace_name, collection_name, api_key, verbose)  # Populate "fields" property
                    col_pbar.update(1)
        
        # Save each endpoint's data to a separate JSON file
        with open(f"rockset_org/rockset_{endpoint}.json", "w") as f:
            json.dump(data, f, indent=2)
        
        pbar.update(1)

tqdm.write("Rockset org metadata created in the 'rockset_org' directory.")
