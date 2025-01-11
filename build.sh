#!/bin/bash

layouts=('us' 'ru' 'gr' 'il')

head='xkb_symbols "basic" {'
caps_pre='key <CAPS> { [ VoidSymbol, Caps_Lock ], actions[Group1] = [ LockGroup(group='
caps_post='), LockMods(mods=Lock) ] };'

rm -rf build
mkdir build

for layout in ${layouts[@]}
do
    echo "Building layout '$layout'..."
    mkdir build/$layout
    klfc layouts/base.json layouts/numpad.json layouts/$layout.json layouts/diacritics.json --xkb build/$layout
    if [ ! -f build/$layout/symbols/$layout ]
    then
        echo 'Error!'
        exit 1
    fi
    # Add switching between the first two layouts by CapsLock:
    [[ $layout = ${layouts[0]} ]] && next_layout='2' || next_layout='1'
    caps_action="    $caps_pre$next_layout$caps_post"
    sed -i "s/$head/$head\n$caps_action/" build/$layout/symbols/$layout
done

# Run the Python scripts
python3 generate_matches.py
# python3 generate_layout_data.py

# Install layouts if started with -i flag
getopts 'i' option
if [ $option = 'i' ]
then
    for layout in ${layouts[@]}
    do
        echo "Installing layout '$layout'..."
        build/$layout/install-system.sh
    done
    
    echo "Copying match files into Espanso config directory..."
    mkdir ~/.config/espanso/match
    rm -f ~/.config/espanso/match/*.yml
    cp -f matches/*.yml ~/.config/espanso/match/
    
    # echo "Copying scripts into Espanso config directory..."
    # mkdir ~/.config/espanso/scripts
    # rm -f ~/.config/espanso/scripts/*
    # cp -f scripts/* ~/.config/espanso/scripts/
fi

echo 'Done.'
