# This script generates the auto-generated `scripts/layouts.pkl` file
# using the data from `layouts/*.json`.

from dataclasses import dataclass
from typing import Any, Iterable
import re
import json
import pickle


common_filenames = ['base', 'diacritics']
layout_filenames = ['us', 'ru', 'gr', 'il']


@dataclass
class KlfcKey:
    pos: str
    letters: list[str]
    shortcutPos: str | None = None
    shiftlevels: list[str] | None = None
    capslock: bool | None = None
    filter: str | None = None


@dataclass
class KlfcLayout:
    fullName: str | None = None
    name: str | None = None
    copyright: str | None = None
    company: str | None = None
    localeId: str | None = None
    version: str | None = None
    description: str | None = None
    qwertyShortcuts: bool | None = None
    filter: str | None = None
    shiftlevels: list[str] | None = None
    keys: list[KlfcKey] | None = None
    singletonKeys: list[str] | None = None  # actually, tuple[str, str]
    # TODO:
    # customDeadKeys
    # variants
    # mods


def json_to_klfc(d: dict[Any, Any]) -> KlfcLayout | KlfcKey:
    if 'pos' in d:
        return KlfcKey(**d)
    else:
        return KlfcLayout(**d)


def get_klfc_layout(filename: str) -> KlfcLayout:
    with open(f'layouts/{filename}.json', 'r') as file:
        lines = file.readlines()
        # remove comments
        lines = [l for l in lines if not re.match(r'^\s*//', l)]
        return json.loads(''.join(lines), object_hook=json_to_klfc)


LayoutDict = dict[tuple[str, str], str]
""" (pos, level) -> letter """


def get_layout_dict(layout_sequence: Iterable[KlfcLayout]) -> LayoutDict:
    layout_dict = dict()
    
    for layout in layout_sequence:
        if layout.keys is None:
            continue
        
        for key in layout.keys:
            # TODO: make 'Shift+AltGr' equal 'AltGr+Shift'
            levels = key.shiftlevels or layout.shiftlevels or []
            for level, letter in zip(levels, key.letters):
                layout_dict[(key.pos, level)] = letter
    
    return layout_dict


def get_layout_dicts() -> dict[str, LayoutDict]:
    common_layouts = [get_klfc_layout(name) for name in common_filenames]
    layout_dicts = dict()
    
    for name in layout_filenames:
        layout = get_klfc_layout(name)
        layout_sequence = [*common_layouts, layout]
        layout_dict = get_layout_dict(layout_sequence)
        layout_dicts[name] = layout_dict
    
    return layout_dicts


if __name__ == '__main__':
    layout_dicts = get_layout_dicts()
    with open('scripts/layouts.pkl', 'wb') as output:
        pickle.dump(layout_dicts, output)
