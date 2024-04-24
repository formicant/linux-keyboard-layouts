# linux-keyboard-layouts

My _XKB_ keyboard layouts and _Espanso_ configuration.

Tested on _Arch Linux_, _KDE Plasma_, _X11_.


## Dependencies

- [Keyboard Layout Files Creator](https://github.com/39aldo39/klfc) (`klfc`)
  
  Converts _.json_ layout description files into _XKB_ files and creates install scripts.

- [_Espanso_](https://espanso.org)
  
  Automatically replaces character strings according to the given patterns while typing.
  
  Should be run as a service:
  ``` bash
  espanso service register
  espanso service start
  ```

## Building and installing

To build the layouts, run
``` bash
./build.sh
```
The script
- creates `build` directory,
- converts the _json_ files into _XKB_ format using `klfc`,
- adds lines to the _XKB_ files to make _CapsLock_ switch between the first two layouts,
- runs `generate_matches.py` to generate `matches/-generated-*.yml` files.

---

To build and install the layouts, run
``` bash
./build.sh -i
```
- installs the _XKB_ layouts,
- copies the match files into the Espanso config directory.

Will ask for your sudo password.

A reboot might be needed to apply the new layouts.

**Warning!** The installed layouts replace the default variants of the corresponding system layouts!
**TODO:** Install the layouts as new variants.


## Contents

- `layouts` directory with layout description _json_ files:
  - `base.json` — non-alphabetical characters used in all layouts
  - `diacritics.json` — diacritical marks used in all layouts
  - `us.json` — a US English-based Latin script layout
  - `ru.json` — a Russian-based Cyrillic script layout
  - `gr.json` — a nontraditional Greek layout
  - `il.json` — a nontraditional Hebrew layout
- `matches` directory with _Espanso_ match description _yaml_ files:
  - `-generated-*.yml` — automatically generated matches based on Unicode character data
  - `*.yml` — manually written matches
- `generate_matches.py` — script generating `-generated-*.yml` matches
- `build.sh` — build script


## Notes

- `Extend+PageUp`, `Extend+PageDown` do not work properly. So I used `Extend+Q` for superscript and `Extend+W` for subscript.
