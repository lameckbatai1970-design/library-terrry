#!/usr/bin/env python3
"""
Main entry point for the Library Management System.

This script can run either the terminal CLI (default) or the GUI app.

Usage:
    python main.py          # CLI (default)
    python main.py --gui    # Launch GUI application
"""

import argparse

from src.cli import LibraryCLI


def main():
    """Run the Library Management System."""
    parser = argparse.ArgumentParser(description="Library Management System")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI application")
    args = parser.parse_args()

    if args.gui:
        try:
            from gui import main as gui_main
        except ImportError:
            print("ERROR: Failed to import GUI module. Make sure you are running from the project root.")
            return

        gui_main()
    else:
        cli = LibraryCLI()
        cli.run()


if __name__ == "__main__":
    main()
