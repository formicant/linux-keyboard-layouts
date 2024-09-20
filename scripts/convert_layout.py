from xclip import get_selection_text
from collections import defaultdict
from os import path
import pickle


script_dir = path.dirname(path.realpath(__file__))
layouts_pkl = path.join(script_dir, 'layouts.pkl')


LayoutDict = dict[tuple[str, str], str]
""" { (pos, level): letter } """

LetterDict = dict[str, dict[str, list[tuple[str, str]]]]
""" { letter: { layout: [(pos, level)] } } """


def get_layout_dicts(pkl_path: str) -> dict[str, LayoutDict]:
    with open(pkl_path, 'rb') as file:
        return pickle.load(file)


def get_letter_dict(layout_dicts: dict[str, LayoutDict]) -> LetterDict:
    letter_dict: LetterDict = defaultdict(lambda: defaultdict(list))
    for layout, layout_dict in layout_dicts.items():
        for (pos, level), letter in layout_dict.items():
            letter_dict[letter][layout].append((pos, level))
    return letter_dict


layout_dicts = get_layout_dicts(layouts_pkl)
letter_dict = get_letter_dict(layout_dicts)


def convert_layout(text: str) -> str:
    chars = []
    for char in text:
        layouts = letter_dict[char]
        variants = layouts['us']
        if variants:
            char = layout_dicts['ru'][variants[0]]
        chars.append(char)
    
    return ''.join(chars)


if __name__ == '__main__':
    input_text = get_selection_text()
    output_text = convert_layout(input_text)
    print(output_text)
