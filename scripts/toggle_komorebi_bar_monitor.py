import argparse
import os
import sys
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("monitor", type=int)
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from extension.komorebi_runtime import DEFAULT_KOMOREBI_CONFIG_DIR, KomorebiBarController

    create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    controller = KomorebiBarController(DEFAULT_KOMOREBI_CONFIG_DIR, create_no_window)
    controller.make_toggle_bar_monitor_command(args.monitor)()


if __name__ == "__main__":
    main()
