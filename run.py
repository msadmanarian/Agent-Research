#!/usr/bin/env python3
"""
Convenience launcher for CogniMesh.
Usage:
    python run.py --demo
    python run.py --benchmark
    python run.py --debate
    python run.py --serve [--port 8080]
"""

import os
import sys

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force UTF-8 encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from agent_research.cli import main

if __name__ == "__main__":
    main()
