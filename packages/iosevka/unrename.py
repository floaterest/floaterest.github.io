#!/usr/bin/env python
import os
import re
import json
from argparse import ArgumentParser

import fontforge

weight = re.compile(r'(heavy|(extra|semi)bold|medium|thin)')
light = re.compile(r'(extralight|light)')

data = {}

def to_names(filename: str) -> (str, str, str, str):
    """
    generate names from font's filename
    :return: fontfamily, fontname, fullname, filename
    """
    full = ['Iosevka', 'Custom']
    family = full[:]
    filename = filename.lower()
    if 'extended' in filename:
        full.append('Extended')
        family.append('Ext')
    if w := weight.search(filename):
        full.append(w.group())
        family.append(w.group())
    elif l := light.search(filename):
        full.append(l.group())
        # family.append(l.group().lower().replace('light','lite').capitalize())
        family.append(l.group().lower().capitalize())
    if 'italic' in filename:
        full.append('Italic')
    if 'bold' in filename:
        full.append('Bold')
    name = full[:]
    family.append('NF')
    name.append('NF')
    full.extend(['Nerd', 'Font'])
    return ' '.join(family), '-'.join(name), ' '.join(full), '-'.join(name).lower()


def new_sfnt(sfnt, family, font, full):
    replace = {
        "Family": family,
        "UniqueID": font,
        "Fullname": full,
        "Preferred Family": family,
        "WWS Family": family,
    }
    res = []
    for name in sfnt:
        if name[1] in replace:
            res.append((name[0], name[1], replace[name[1]]))
        else:
            res.append(name)
    return tuple(res)

def main(srcdir: str, destdir: str):
    os.makedirs(destdir, exist_ok=True)
    for file in os.listdir(srcdir):
        ext = os.path.splitext(file)[1]
        f = fontforge.open(os.path.join(srcdir, file))
        f.familyname, f.fontname, f.fullname, filename = to_names(file)
        f.sfnt_names = new_sfnt(f.sfnt_names, f.familyname, f.fontname, f.fullname)

        if f.familyname in data:
            data[f.familyname].append([f.fontname, f.fullname, f.sfnt_names])
        else:
            data[f.familyname] = [[f.fontname, f.fullname, f.sfnt_names]]
        f.generate(os.path.join(destdir, f'{filename}{ext}'))

    with open(os.path.join(destdir, 'iosevka.json'),'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('src', help='source directory')
    parser.add_argument('dest', help='destination directory')
    args = parser.parse_args()
    main(args.src, args.dest)
