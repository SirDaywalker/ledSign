"""
deploy.py – Automatisches Deployment auf den Raspberry Pi Pico W
================================================================
Verwendung:
    python deploy.py                    # COM-Port wird automatisch erkannt, keine optionalen Uploads
    python deploy.py --port COM3        # COM-Port manuell angeben
    python deploy.py --optional-upload  # Optionale Dateien werden mit hochgeladen
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

LOCAL_ROOT = Path(__file__).parent

ALWAYS_UPLOAD: list[str] = [
    "main.py",
    "boot.py",
    "pyproject.toml"
]

ALWAYS_UPLOAD_DIRS: list[str] = [
    "lib",
    "lib/static"
]

OPTIONAL_UPLOAD: list[str] = [
    "settings.py"
]

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def run_command(cmd: list[str]) -> subprocess.CompletedProcess:
    """
    Runs a command in the shell and returns its completed process.

    Args:
        cmd (list[str]): The command to execute in the shell, provided as a list
        where the first element is the command itself and the remaining are its
        arguments.

    Returns:
        subprocess.CompletedProcess: An object containing information about the
        executed process including its output, error messages, and return code.
    """
    return subprocess.run(cmd, capture_output=True, text=True)


def run_mpremote_command(port: str | None, *args: str) -> subprocess.CompletedProcess:
    """
    Executes an mpremote command using a subprocess and returns its result.

    Parameters:
        port (str | None): The port to which `mpremote` should connect. If None,
            no port connection is included in the command.
        *args (str): Additional arguments to pass to the `mpremote` command.

    Returns:
        subprocess.CompletedProcess: The result of executing the `mpremote` command.
    """
    cmd = [sys.executable, "-m", "mpremote"]
    if port:
        cmd += ["connect", port]
    cmd += list(args)
    return run_command(cmd)


def create_dir_on_pico(port: str | None, remote_dir: str) -> None:
    """
    Creates a directory on the Raspberry Pi Pico.

    Arguments:
        port (str | None): The serial port to communicate with the Raspberry Pi Pico.
            If None, it will attempt to find the device automatically.
        remote_dir (str): The path of the directory to be created on the Raspberry Pi
            Pico.

    Returns:
        None
    """
    run_mpremote_command(port, "fs", "mkdir", remote_dir)


def ensure_dirs_on_pico(port: str | None, remote_path: str) -> None:
    """
    Ensures that a directory tree structure exists on the Raspberry Pi Pico.

    Parameters:
        port : str | None
            The port where the Pico device is connected. If None, the default
            connection is used.
        remote_path : str
            The directory path on the Pico device to ensure. The path should
            consist of directories separated by forward slashes.

    Returns:
        None
    """
    parts = remote_path.split("/")
    for i in range(1, len(parts)):
        create_dir_on_pico(port, "/".join(parts[:i]))


def upload_file_to_pico(port: str | None, local_path: Path, remote_path: str) -> bool:
    """
    Uploads a file to the Raspberry Pi Pico, ensuring the necessary directories exist before transferring the file.

    Parameters:
        port (str | None): The communication port to connect to the Pico device. Specify None to use the default port.
        local_path (Path): The path to the local file to be uploaded.
        remote_path (str): The target path on the Pico device where the file will be stored.

    Returns:
        bool: True if the upload was successful, otherwise False.
    """
    ensure_dirs_on_pico(port, remote_path)
    result = run_mpremote_command(port, "fs", "cp", str(local_path), f":{remote_path}")
    return result.returncode == 0


def map_path_relative(path: Path) -> tuple[Path, str]:
    """
    Maps the given path relatively to the local project root (equivalent to the path on the Raspberry Pi Pico) and returns both.

    Parameters:
    path : Path
        The input path to be processed.

    Returns:
    tuple[Path, str]
        A tuple containing:
        - The original input path.
        - The relative path to the local project (path on the Raspberry Pi Pico) as a string.
    """
    return path, str(path.relative_to(LOCAL_ROOT)).replace("\\", "/")


def collect_relative_dir_files(directory: Path) -> list[tuple[Path, str]]:
    """
    Collects all files in a given directory and returns a list of tuples, where each tuple
    contains the path of a local file and its relative path on the Raspberry Pi Pico as a string.

    Parameters:
        directory (Path): The root directory to search for files.

    Returns:
        list[tuple[Path, str]]: A list of tuples where each tuple contains the
            path of a local file and its string representation on the Raspberry Pi Pico.
    """
    files = []
    for local_path in sorted(directory.rglob("*")):
        if not local_path.is_file():
            continue

        mapped_file_path = map_path_relative(local_path)
        files.append(mapped_file_path)
    return files


def upload_files(port: str | None, files_to_upload: list[tuple[Path, str]]) -> None:
    """
    Uploads a list of files to the Raspberry Pi Pico.

    Parameters:
        port (str | None): The port identifier for the target device. This determines where the files
                           will be uploaded.
        files_to_upload (list[tuple[Path, str]]): A list of tuples where each tuple contains the local
                                                  file path (as a Path object) and the remote file path
                                                  (as a string).

    Returns:
        None
    """
    for local_path, remote_path in files_to_upload:
        if not local_path.exists():
            print(f"  ⚠  {local_path}/ lokal nicht gefunden, übersprungen.")
            continue
        print(f"  {remote_path}", end=" ... ", flush=True)
        print("✓ hochgeladen" if upload_file_to_pico(port, local_path, remote_path) else "✗ FEHLER!")


# ---------------------------------------------------------------------------
# Upload-Logik
# ---------------------------------------------------------------------------

def upload_standard_files(port: str | None) -> None:
    print("\n[1/1] Lade Code-Dateien hoch …")

    files_to_upload = []

    for filename in ALWAYS_UPLOAD:
        files_to_upload.append(map_path_relative(LOCAL_ROOT / filename))

    for dir_name in ALWAYS_UPLOAD_DIRS:
        files_to_upload.append(collect_relative_dir_files(LOCAL_ROOT / dir_name))

    upload_files(port, files_to_upload)


def upload_optional_files(port: str | None) -> None:
    print("\n[+] Lade optionale Dateien hoch (--force-upload) …")

    files_to_upload = []

    for filename in OPTIONAL_UPLOAD:
        files_to_upload.append(map_path_relative(LOCAL_ROOT / filename))

    upload_files(port, files_to_upload)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Deployment-Skript für den Raspberry Pi Pico W")
    parser.add_argument("--port", "-p", default=None,
                        help="COM-Port des Pico (z.B. COM3). Wird auto-erkannt, wenn weggelassen.")
    parser.add_argument("--optional-upload", "-o", action="store_true", default=False,
                        help="settings.py immer hochladen und überschreiben, auch wenn bereits vorhanden.")
    args = parser.parse_args()

    check = run_command([sys.executable, "-m", "mpremote", "--version"])
    if check.returncode != 0:
        print("✗ mpremote nicht gefunden. Bitte installiere alle benötigten Pakete: pip install -r requirements.txt")
        sys.exit(1)

    print(f"╔══════════════════════════════════════════╗")
    print(f"║   Pico W Deployment – ledSign            ║")
    print(f"╚══════════════════════════════════════════╝")
    print(f"  Port:         {args.port or 'auto'}")
    print(f"  Lokales Repo: {LOCAL_ROOT}")

    upload_standard_files(args.port)
    if args.optional_upload:
        upload_optional_files(args.port)

    print("\n✓ Deployment abgeschlossen.")


if __name__ == "__main__":
    main()