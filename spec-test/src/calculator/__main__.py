"""Entry point for running calculator as a module.

This allows the calculator to be run with:
    python -m calculator <args>
"""

import sys

from calculator.cli import main

if __name__ == "__main__":
    sys.exit(main())
