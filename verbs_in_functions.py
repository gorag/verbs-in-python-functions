import argparse
import ast
import os

from collections import Counter
from nltk import pos_tag


def get_files_with_extension(
        dir_to_start, number_of_files=None):
    file_names = []
    for _dir_name, _dirs, _files in os.walk(dir_to_start):
        for file in _files:
            if file.endswith('.py'):
                file_names.append(os.path.join(_dir_name, file))
                if len(file_names) == number_of_files:
                    return file_names
    return file_names


def get_valid_trees(content_of_files: "dict"):
    code_trees = []
    for file_name, content in content_of_files.items():
        try:
            code_tree = ast.parse(content)
            code_trees.append(code_tree)
        except SyntaxError as e:
            print("{} {}".format(str(e), file_name))
    return code_trees


def get_function_names(trees):
    nodes_names = flat([[node.name.lower() for node in ast.walk(tree)
                         if isinstance(node, ast.FunctionDef)]
                        for tree in trees])
    function_names = [names for names in nodes_names if not (
        names.startswith('__') and names.endswith('__'))]
    return function_names


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    return pos_tag([word])[0][1] == 'VB'


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def read_file(file_names):
    contents_of_files = {}
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as file_handler:
            contents_of_files[file_name] = file_handler.read()
    return contents_of_files


def find_top_verbs_in_python_functions(
        path_name, number_of_files=None, num_top_verbs=10):
    files = get_files_with_extension(path_name, number_of_files)
    read = read_file(files)
    trees = get_valid_trees(read)
    function_names = get_function_names(trees)
    verbs = flat(get_verbs_from_function_name(
        function_name) for function_name in function_names)
    top_verbs = Counter(verbs).most_common(num_top_verbs)

    print("found %d file(s), valid %d file(s)" % (len(files), len(trees)))
    print("found %d function(s) of which %d verb(s), %d unique"
          % (len(function_names), len(verbs), len(set(verbs))))
    print("top %d verbs are:" % num_top_verbs)
    for item in top_verbs:
        print(item)


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value)
    return ivalue


def create_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', nargs='?')
    parser.add_argument('-f', type=check_positive, default=None)
    parser.add_argument('-t', type=check_positive, default=10)

    return parser


if __name__ == "__main__":
    import sys

    _parser = create_parser()
    _path = _parser.parse_args(sys.argv[1:])
    if not os.path.exists(_path.path):
        raise argparse.ArgumentTypeError("path %s is not exists" % _path.path)

    _num_files = _parser.parse_args(sys.argv[2:])
    _top_verbs = _parser.parse_args(sys.argv[3:])

    find_top_verbs_in_python_functions(_path.path, _num_files.f, _top_verbs.t)
