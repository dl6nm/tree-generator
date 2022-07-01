import json

import pytest

from path_tree_generator import PathTree
from path_tree_generator.models.list_entries import ListEntry


def test_path_tree_dict(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        paths_as_posix=True,
    )

    data_file = (shared_datadir/'data.json')
    expected_dict = ListEntry.parse_file(data_file)

    assert pt.dict() == expected_dict.dict()


def test_path_tree_json(shared_datadir):
    pt = PathTree(
        root_dir=shared_datadir,
        paths_as_posix=True,
    )
    tree_json = json.loads(pt.json(exclude_unset=True))

    data_file = (shared_datadir/'data.json')
    expected_json = json.load(data_file.open(encoding='utf-8'))

    assert tree_json == expected_json


@pytest.mark.parametrize(
    argnames='expected_hr_tree',
    argvalues=[
        [
            '[data]',
            '├── data.json',
            '├── data.tree',
            '├── [myDirectory-1]',
            '│   ├── myFile.txt',
            '│   └── [subdirectory]',
            '│       └── green.gif',
            '└── [myDirectory-2]',
            '    ├── [subdirectory1]',
            '    │   └── green.gif',
            '    └── [subdirectory2]',
            '        ├── myFile.txt',
            '        └── myFile2.txt'
        ]
    ],
    ids=['human readable']
)
def test_path_tree_human_readable(shared_datadir, expected_hr_tree):
    pt = PathTree(root_dir=shared_datadir)

    assert pt.human_readable() == expected_hr_tree

    data_file = (shared_datadir/'data.tree')
    expected_data = data_file.open(encoding='utf-8').read()

    actual_data = pt.human_readable()
    actual_data.append('')  # append an empty line for getting rid of a line-break problem while testing
    assert '\n'.join(actual_data) == expected_data


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('wrap_with_root_dir', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_dict_parameters(relative_paths, wrap_with_root_dir, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        wrap_with_root_dir=wrap_with_root_dir,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.dict(), dict)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('wrap_with_root_dir', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_json_parameters(relative_paths, wrap_with_root_dir, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        wrap_with_root_dir=wrap_with_root_dir,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.json(), str)


@pytest.mark.parametrize('relative_paths', [True, False])
@pytest.mark.parametrize('wrap_with_root_dir', [True, False])
@pytest.mark.parametrize('paths_as_posix', [True, False])
def test_path_tree_human_readable_parameters(relative_paths, wrap_with_root_dir, paths_as_posix):
    pt = PathTree(
        root_dir='/not/relevant/for/this/test',
        relative_paths=relative_paths,
        wrap_with_root_dir=wrap_with_root_dir,
        paths_as_posix=paths_as_posix,
    )
    assert isinstance(pt.human_readable(), list)
