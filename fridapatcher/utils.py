import os
import platform

def get_default_download_dir():
    system = platform.system()
    if system in ["Windows", "Darwin", "Linux"]:
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        return os.path.expanduser("~")