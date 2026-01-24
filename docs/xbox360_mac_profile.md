# Xbox360MacProfile
# Extracted from Assembly-CSharp.dll using monodis

## Profile Configuration

Name: XBox 360 Controller
Meta: XBox 360 Controller on Mac
Platform: OS X

## JoystickNames Array (6 elements)

Index | String                                                | Length
------|-------------------------------------------------------|-------
0     | (empty)                                               | 0
1     | Microsoft Wireless 360 Controller                     | 33
2     | Mad Catz, Inc. Mad Catz FPS Pro GamePad               | 39
3     | Mad Catz, Inc. MadCatz Call of Duty GamePad           | 43
4     | ©Microsoft Corporation Controller                     | 33
5     | ©Microsoft Corporation Xbox Original Wired Controller | 53

Note: © = \xa9 (copyright symbol, Unicode U+00A9)

## JoystickRegex

Pattern: "360"
Length: 3 characters (too short to patch for "GamePad")

## String Positions in DLL

0x1b9f16  Microsoft Wireless 360 Controller
0x1b9f5a  Mad Catz, Inc. Mad Catz FPS Pro GamePad
0x1b9faa  Mad Catz, Inc. MadCatz Call of Duty GamePad
0x1ba002  ©Microsoft Corporation Controller
0x1ba044  ©Microsoft Corporation Xbox Original Wired Controller


## Solution

Patch the JoystickNames to recognize Steam Input controllers:

Original                                      | Replacement           | Chars
----------------------------------------------|-----------------------|------
Microsoft Wireless 360 Controller             | Microsoft GamePad-1   | 33→19
Mad Catz, Inc. Mad Catz FPS Pro GamePad       | Microsoft GamePad-2   | 39→19
Mad Catz, Inc. MadCatz Call of Duty GamePad   | Microsoft GamePad-3   | 43→19
©Microsoft Corporation Controller             | Microsoft GamePad-4   | 33→19

## Code Reference

From monodis output:

```il
.method public hidebysig specialname rtspecialname
       instance default void '.ctor' ()  cil managed
{
    // Method begins at RVA 0x2f010
    // Code size 896 (0x380)

    IL_0007:  ldstr "XBox 360 Controller"
    IL_000c:  call instance void class InControl.InputDeviceProfile::set_Name(string)

    IL_0012:  ldstr "XBox 360 Controller on Mac"
    IL_0017:  call instance void class InControl.InputDeviceProfile::set_Meta(string)

    IL_0033:  ldstr "OS X"
    IL_0039:  call instance void class InControl.InputDeviceProfile::set_IncludePlatforms(string[])

    // JoystickNames array (6 elements)
    IL_003f:  ldc.i4.6
    IL_0040:  newarr [mscorlib]System.String
    IL_004f:  ldstr "Microsoft Wireless 360 Controller"
    IL_0057:  ldstr "Mad Catz, Inc. Mad Catz FPS Pro GamePad"
    IL_005f:  ldstr "Mad Catz, Inc. MadCatz Call of Duty GamePad"
    IL_0067:  ldstr "©Microsoft Corporation Controller"
    IL_006f:  ldstr "©Microsoft Corporation Xbox Original Wired Controller"

    // JoystickRegex
    IL_007b:  ldstr "360"
}
```
