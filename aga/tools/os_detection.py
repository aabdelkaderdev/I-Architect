import platform
import sys

def get_planturl_binary_path() -> str:
    """
    Returns the path to the correct planturl binary based on the OS and architecture.
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        return "tools/planturl/Bin/windows-msvc/planturl.exe"
    elif system == "darwin":
        if machine == "arm64":
            return "tools/planturl/Bin/aarch64-apple-darwin/planturl"
        else:
            return "tools/planturl/Bin/apple-darwin/planturl"
    elif system == "linux":
        # Check if it's alpine/musl or glibc. A simple heuristic is checking if it's Alpine.
        # But usually we check for musl.
        # Given the requirements: glibc vs musl.
        # We can check ldd or just look at python's sys platform or os.
        import os
        if os.path.exists('/lib/ld-musl-x86_64.so.1') or os.path.exists('/lib/libc.musl-x86_64.so.1'):
            return "tools/planturl/Bin/linux-musl/planturl"
        else:
            return "tools/planturl/Bin/linux-gnu/planturl"
    else:
        raise OSError(f"Unsupported operating system: {system}")
