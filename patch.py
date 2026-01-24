#!/usr/bin/env python3
"""
Tricky Towers Steam Input Patch

Patches Assembly-CSharp.dll to recognize Steam Input's virtual controllers
("Microsoft GamePad-1", "Microsoft GamePad-2", etc.) as Xbox 360 controllers.

Usage:
    python3 patch.py [--restore] [path/to/Assembly-CSharp.dll]
"""

import logging
import shutil
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

DEFAULT_DLL = (
    Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "common"
    / "Tricky Towers" / "TrickyTowers.app" / "Contents" / "Resources" / "Data" / "Managed"
    / "Assembly-CSharp.dll"
)

# Xbox360MacProfile JoystickNames to replace with Steam Input controller names
# Each original string must be >= length of replacement (will be null-padded)
# Note: © = \xa9 (copyright symbol) prefixes some strings in the DLL
PATCHES = [
    ("Microsoft Wireless 360 Controller", "Microsoft GamePad-1"),
    ("Mad Catz, Inc. Mad Catz FPS Pro GamePad", "Microsoft GamePad-2"),
    ("Mad Catz, Inc. MadCatz Call of Duty GamePad", "Microsoft GamePad-3"),
    ("\xa9Microsoft Corporation Controller", "Microsoft GamePad-4"),
]


def patch_string(data: bytearray, old_str: str, new_str: str) -> bool:
    """Replace a .NET User String in the DLL."""
    old_utf16 = old_str.encode("utf-16-le")
    new_utf16 = new_str.encode("utf-16-le")

    if len(new_utf16) > len(old_utf16):
        log.error("'%s' is longer than '%s'", new_str, old_str)
        return False

    old_length_byte = len(old_utf16) + 1
    new_length_byte = len(new_utf16) + 1

    pattern = bytes([old_length_byte]) + old_utf16
    pos = data.find(pattern)

    if pos == -1:
        new_pattern = bytes([new_length_byte]) + new_utf16
        if new_pattern in data:
            log.info("  Already patched: '%s'", new_str)
            return True
        return False

    data[pos] = new_length_byte
    data[pos + 1:pos + 1 + len(new_utf16)] = new_utf16
    for i in range(len(new_utf16), len(old_utf16) + 1):
        data[pos + 1 + i] = 0x00

    log.info("  Patched: '%s' -> '%s'", old_str, new_str)
    return True


def patch_dll(dll_path: Path) -> bool:
    backup = dll_path.with_suffix(".dll.bak")

    if not dll_path.exists():
        log.error("DLL not found: %s", dll_path)
        return False

    if not backup.exists():
        shutil.copy2(dll_path, backup)
        log.info("Backup: %s", backup.name)

    data = bytearray(dll_path.read_bytes())

    patched = sum(1 for old, new in PATCHES if patch_string(data, old, new))

    if patched == 0:
        log.error("No strings found to patch")
        return False

    dll_path.write_bytes(data)
    log.info("Patched %d/%d controller names", patched, len(PATCHES))
    return True


def restore_dll(dll_path: Path) -> bool:
    backup = dll_path.with_suffix(".dll.bak")
    if not backup.exists():
        log.error("No backup found")
        return False
    shutil.copy2(backup, dll_path)
    log.info("Restored from backup")
    return True


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dll_path = Path(args[0]) if args else DEFAULT_DLL

    log.info("DLL: %s", dll_path)

    if "--restore" in sys.argv:
        return 0 if restore_dll(dll_path) else 1

    if patch_dll(dll_path):
        log.info("\nEnable Steam Input: Steam -> Tricky Towers -> Properties -> Controller")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
