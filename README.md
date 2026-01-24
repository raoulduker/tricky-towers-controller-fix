# Tricky Towers Steam Input Patch (macOS)

Fixes controller support on macOS by patching the game to recognize Steam Input's virtual controllers.

## Problem

Tricky Towers uses InControl for input handling. On macOS, Steam Input presents controllers as "Microsoft GamePad-1", "Microsoft GamePad-2", etc. These names don't match any built-in InControl profile, causing controllers to appear as "Unknown Device".

## Solution

Patches `Assembly-CSharp.dll` to replace Xbox360MacProfile's JoystickNames with Steam Input controller names:

| Original | Replacement |
|----------|-------------|
| Microsoft Wireless 360 Controller | Microsoft GamePad-1 |
| Mad Catz, Inc. Mad Catz FPS Pro GamePad | Microsoft GamePad-2 |
| Mad Catz, Inc. MadCatz Call of Duty GamePad | Microsoft GamePad-3 |
| ©Microsoft Corporation Controller | Microsoft GamePad-4 |

## Usage

### GUI (recommended)

```bash
python3 patch_gui.py
```

Automatically detects Steam installation, or lets you select the app manually.

### Command Line

```bash
python3 patch.py                        # Apply patch (default Steam path)
python3 patch.py /path/to/dll           # Apply patch (custom path)
python3 patch.py --restore              # Restore original
python3 patch.py --restore /path/to/dll # Restore (custom path)
```

### After Patching

Enable Steam Input:
1. Steam → Right-click Tricky Towers -> Properties -> Controller
2. Select "Enable Steam Input"

## Tested With

- Tricky Towers (unity.WeirdBeard.Tricky Towers)
- Unity Player 5.5.1p3 (828893732fe0)

## Notes

- Supports up to 4 controllers
- Backup created automatically (`Assembly-CSharp.dll.bak`)
- Game updates will overwrite the patch
- See `docs/` for technical details
