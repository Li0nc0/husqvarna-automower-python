#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

AUTH_BASE = "https://api.authentication.husqvarnagroup.dev/v1"
TOKEN_URL = f"{AUTH_BASE}/oauth2/token"

AM_BASE = "https://api.amc.husqvarna.dev/v1"
MOWERS_URL = f"{AM_BASE}/mowers"

class HusqvarnaAPIError(Exception):
    pass

def load_config(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise HusqvarnaAPIError(f"No config file in : {path}")
    try:
        with open(p, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        raise HusqvarnaAPIError(f"JSON Error {path}: {e}")

    for k in ("app_key", "app_secret"):
        if k not in cfg or not cfg[k]:
            raise HusqvarnaAPIError(f"Missing key '{k}' in {path}")
    return cfg

def get_access_token(app_key: str, app_secret: str) -> str:
    data = {
        "grant_type": "client_credentials",
        "client_id": app_key,
        "client_secret": app_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(TOKEN_URL, data=data, headers=headers, timeout=15)
    if r.status_code != 200:
        raise HusqvarnaAPIError(f"Erreur token ({r.status_code}) : {r.text}")
    token = r.json().get("access_token")
    if not token:
        raise HusqvarnaAPIError("Invalid token (any d'access_token).")
    return token

def get_mowers(access_token: str, app_key: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": app_key,
        "Authorization-Provider": "husqvarna",
        "Accept": "application/vnd.api+json",  # required for /mowers
    }
    r = requests.get(MOWERS_URL, headers=headers, timeout=15)
    if r.status_code != 200:
        raise HusqvarnaAPIError(f" Mowers errors ({r.status_code}) : {r.text}")
    return r.json().get("data", [])

def get_mower_detail(mower_id: str, access_token: str, app_key: str):
    url = f"{AM_BASE}/mowers/{mower_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": app_key,
        "Authorization-Provider": "husqvarna",
        "Accept": "application/vnd.api+json",
    }
    r = requests.get(url, headers=headers, timeout=15)
    return r.json() if r.status_code == 200 else {"error": r.status_code, "body": r.text}

#def get_mower_messages(mower_id: str, access_token: str, app_key: str):
#    url = f"{AM_BASE}/mowers/{mower_id}/messages"
#    headers = {
#        "Authorization": f"Bearer {access_token}",
#        "X-Api-Key": app_key,
#        "Authorization-Provider": "husqvarna",
#        "Accept": "application/json",
#    }
#    r = requests.get(url, headers=headers, timeout=15)
#    return r.json() if r.status_code == 200 else {"error": r.status_code, "body": r.text}

def main():
    # Arg 1 : config file (default config.json)
    # Arg 2 : output file (default data.json)
    config_path = sys.argv[1] if len(sys.argv) > 1 else "./config.json"
    outpath = sys.argv[2] if len(sys.argv) > 2 else "./data.json"

    cfg = load_config(config_path)
    access_token = get_access_token(cfg["app_key"], cfg["app_secret"])
    mowers = get_mowers(access_token, cfg["app_key"])

    timestamp = datetime.now(timezone.utc).isoformat()

    results = []
    for m in mowers:
        mower_id = m.get("id")
        if not mower_id:
            continue
        detail = get_mower_detail(mower_id, access_token, cfg["app_key"])
	#Not available on Husqvarna 315X        
	#messages = get_mower_messages(mower_id, access_token, cfg["app_key"])
        results.append({
            "mower_id": mower_id,
            "timestamp": timestamp,
            "detail": detail,
            #"messages": messages,
        })

    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    #print(f" Details written in {outpath}")

if __name__ == "__main__":
    try:
        main()
    except HusqvarnaAPIError as e:
        print(f"[API ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"[NETWORK ERROR] {e}", file=sys.stderr)
        sys.exit(2)

