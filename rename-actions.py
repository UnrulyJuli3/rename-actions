import os
import re
import shutil
from typing import Any

import requests

paths = [
    "C:\\Program Files (x86)\\Steam\\steamapps\\common\\The Jackbox Party Pack 3\\games\\TriviaDeath",
    "C:\\Program Files (x86)\\Steam\\steamapps\\common\\The Jackbox Party Pack 4\\games\\Bracketeering"
]

create_backup = True

remote_url = "https://juli3.s3.us-west-1.amazonaws.com"

swf_re = r"\.swf$"
print("Fetching tags")
tags: dict[str, str] = requests.get(f"{remote_url}/tags.json").json()


def get_actions_names(tag: str):
    actions_names: dict[str, str] = {}
    print(f"[{tag}] Fetching data")
    data: dict[str, dict[str, Any]] = requests.get(
        f"{remote_url}/games/{tag}/talkshow/data.json"
    ).json()
    start_data = data["start"]
    if start_data is not None:
        dict_str: str = start_data["dict"]
        packages_data: str = start_data["packages"]
        dictionary = dict_str.split("^")
        packages = packages_data.split("^")
        for package_data in packages:
            parts = package_data.split("|")
            id = parts[0]
            name = dictionary[int(parts[1])]
            # the rest is irrelevant
            actions_names[id] = name
    return actions_names


for path in paths:
    possible_tags = [
        pair[1] for pair in tags.items() if path.replace("\\", "/").endswith(pair[0])
    ]
    if len(possible_tags) >= 1:
        tag = possible_tags[0]
        actions_names = get_actions_names(tag)
        actions_path = os.path.join(path, "TalkshowExport/project", "actions")
        backup_path = os.path.join(path, "TalkshowExport/project", "actions-backup")
        if create_backup and not os.path.exists(backup_path):
            shutil.copytree(actions_path, backup_path)
            print(f"[{tag}] Created backup at TalkshowExport/project/actions-backup")
        for name in os.listdir(actions_path):
            if re.search(swf_re, name, re.IGNORECASE):
                action_id = re.sub(swf_re, "", name, 1, re.IGNORECASE)
                if action_id in actions_names:
                    os.rename(
                        os.path.join(actions_path, name),
                        os.path.join(actions_path, f"{actions_names[action_id]}.swf"),
                    )
                    print(f"[{tag}] {action_id} -> {actions_names[action_id]}")
