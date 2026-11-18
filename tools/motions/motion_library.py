#!/usr/bin/env python3
"""Offline G1 motion inventory and approval commands."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from GuideBot.hardware.g1_motion.assets import *


if __name__ == "__main__":
    sys.exit(main())
