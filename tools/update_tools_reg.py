import hashlib
import json
import os
import subprocess
from typing import Any

import requests


def get_sha256(name: str, url: str) -> str:
    print(f"Calculating SHA256 for {name}")
    subprocess.run(["wget", url], check=True, capture_output=True)
    with open(name, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        f.close()
        os.remove(name)

    return hash_value.lower()


def get_asset_info(asset: dict[str, str], ret: dict[str, Any]) -> None:
    tmp = {"url": asset["browser_download_url"]}
    name = asset["name"]
    key = ""
    if "macos" in name or "osx" in name:
        key = "macos"
    elif "linux" in name:
        key = "linux"
    elif "win" in name:
        key = "windows"
    else:
        return

    if "amd64" in name or "x86_64" in name or "win64" in name:
        key = key + "-amd64"
    elif "arm64" in name or "aarch_64" in name:
        key = key + "-aarch64"
    else:
        return

    digest: str | None = asset["digest"]
    if digest is not None and digest.startswith("sha256:"):
        tmp["sha256"] = digest[7:]
    else:
        tmp["sha256"] = get_sha256(name, tmp["url"])

    ret[key] = tmp


def get_latest_download_info(repo_name: str, info: str) -> dict[str, str] | None:
    print(f"---- Getting {repo_name} --------", flush=True)

    # Construct the GitHub API URL for the latest release
    api_url = f"https://api.github.com/repos/{repo_name}/releases/latest"

    # Set headers for GitHub API (authentication is optional but recommended)
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors

        # Parse the JSON response
        release_data = response.json()
        ver = release_data["tag_name"]
        if f'"version": "{ver}"' in info:
            print(f"{ver} is already exist")
            return None

        ret = {"version": ver}
        # Check if there are any assets in the release
        if "assets" in release_data and len(release_data["assets"]) > 0:
            for a in release_data["assets"]:
                get_asset_info(a, ret)
            print(f"Got {ver}")
            return ret
        else:
            print("No assets found in the latest release.")
            return None

    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print("API rate limit exceeded. Consider using a GitHub Personal Access Token.")
        else:
            print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching release data: {e}")
        return None


if __name__ == "__main__":
    out_name = "tools/tools_reg.bzl"
    separator = "\n#----\n"
    with open(out_name, "r") as f:
        [protoc_info, protoc_c_info] = f.read().split(separator)

    commit_msg = "Update tools"
    need_write = False
    ret = get_latest_download_info("protocolbuffers/protobuf", protoc_info)
    if ret is not None:
        protoc_info = "PROTOC = " + json.dumps(ret, indent=4)
        commit_msg = commit_msg + f" protoc {ret['version']}"
        need_write = True

    ret = get_latest_download_info("JalonWong/protobuf-c-release", protoc_c_info)
    if ret is not None:
        protoc_c_info = "PROTOC_C = " + json.dumps(ret, indent=4)
        commit_msg = commit_msg + f" protoc-gen-c {ret['version']}"
        need_write = True

    if need_write:
        with open(out_name, "w") as f:
            f.write(protoc_info)
            f.write(separator)
            f.write(protoc_c_info)

        with open("commit.txt", "w") as f:
            f.write(commit_msg)
    else:
        print("No changes", flush=True)
