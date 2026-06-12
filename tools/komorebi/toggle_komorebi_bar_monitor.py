import argparse
import sys
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("monitor", type=int)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from extensions.apps.komorebi_runtime import DEFAULT_KOMOREBI_CONFIG_DIR, KomorebiBarController

    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    controller = KomorebiBarController(DEFAULT_KOMOREBI_CONFIG_DIR, create_no_window)
    controller.make_toggle_bar_monitor_command(args.monitor)()


if __name__ == "__main__":
    main()
