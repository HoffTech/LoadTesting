MISSED_SYMBOL = '0'
LOAD_YAML = {
    "phantom": {
        "enabled": True,
        "address": "",
        "ammofile": "./ammo.txt",
        "load_profile": {
            "load_type": "",
            "schedule": ""
        },
        "timeout": "",
        "phantom_http_entity": "30M"
    },
    "bfg": {
        "package": "yandextank.plugins.Bfg",
        "enabled": False,
        "ammofile": "./ammo.line",
        "instances": "10",
        "loop": "100",
        "gun_config": {
            "class_name": "",
            "module_path": "./",
            "module_name": "",
            "host": "",
        },
        "gun_type": "ultimate",
        "load_profile": {
            "load_type": "",
            "schedule": ""
        }
    },
    "console": {
        "enabled": True
    },
    "telegraf": {
        "enabled": False
    },
    "overload": {
        "enabled": True,
        "package": "yandextank.plugins.DataUploader",
        "token_file": "token.txt",
        "job_name": "",
        "job_dsc": ""
    }
}

endpoints = []
