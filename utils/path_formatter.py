import platform


def create_path(mac_path: str):
    """Creates os system paths based on operating system"""
    path = mac_path.replace(" ", "_")
    if platform.system() == "Windows":
        return path.replace("/", "\\")

    return path
