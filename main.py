import json
import requests
import sys
from argparse import ArgumentParser

METADATA_BASE_URL = "http://169.254.169.254/latest/meta-data/"
DYNAMIC_BASE_URL = "http://169.254.169.254/latest/dynamic/"

def get_specific_key(key_path):
    url = f"{METADATA_BASE_URL}{key_path}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return response.text
        return None
    except requests.exceptions.RequestException:
        return None

def get_dynamic_data():
    """Fetch dynamic instance identity document"""
    url = f"{DYNAMIC_BASE_URL}instance-identity/document"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def list_all_keys():
    """List all available metadata keys (non-recursive)"""
    try:
        response = requests.get(METADATA_BASE_URL, timeout=2)
        if response.status_code == 200:
            return response.text.splitlines()
        return []
    except requests.exceptions.RequestException:
        return []

def main():
    parser = ArgumentParser(description="AWS Instance Metadata Query Tool")
    parser.add_argument("-k", "--key", help="Specific metadata key to retrieve (e.g. 'instance-id')")
    parser.add_argument("-l", "--list", action="store_true", help="List all available metadata keys")
    parser.add_argument("-d", "--dynamic", action="store_true", help="Get dynamic instance identity document")
    args = parser.parse_args()

    if args.dynamic:
        data = get_dynamic_data()
        print(json.dumps(data, indent=2))
        return
    
    if args.list:
        keys = list_all_keys()
        print("Available metadata keys:")
        for key in keys:
            print(f"- {key}")
        return
    
    if args.key:
        data = get_specific_key(args.key)
        if data is not None:
            if isinstance(data, (dict, list)):
                print(json.dumps(data, indent=2))
            else:
                print(data)
        else:
            print(f"Key '{args.key}' not found or could not be retrieved", file=sys.stderr)
            sys.exit(1)
    else:
        print("No key specified. Use --list to see available keys or --help for usage.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()