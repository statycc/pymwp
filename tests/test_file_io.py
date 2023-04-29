import os
import json

from pymwp.file_io import default_file_out, save_result, load_result, loc
from pymwp import Relation, Choices, Result, Bound
from pymwp.result import FuncResult


def test_file_out_name_wo_path():
    """Generating output filename from just a filename without path returns
    result with output directory path."""
    input_file = "my_c_file.c"
    out_file = default_file_out(input_file)

    assert out_file == "output/my_c_file.json"


def test_file_out_name_with_path():
    """Generating output filename removes original filepath."""
    input_file = "my_dir/of/files/example.c"
    out_file = default_file_out(input_file)

    assert out_file == "output/example.json"


# noinspection PyUnresolvedReferences
def test_save_relation(mocker):
    """Method generates directory when it does not exist then saves."""
    # mock all built-ins
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    mocker.patch('builtins.open')
    mocker.patch('json.dump')

    result = Result()
    filename = 'fake_path/deep/path/output.txt'
    result.add_relation(
        FuncResult('foo', False, relation=Relation(), choices=Choices()))
    save_result(filename, result)

    # it creates directory path when dir/s do not exist
    os.makedirs.assert_called_once_with('fake_path/deep/path')
    # it saves json
    json.dump.assert_called_once()


def test_load_relation(mocker):
    """Method generates expected object instance."""
    # mock built-ins
    mocker.patch('json.load', return_value={
        "start_time": 1682637184575679000,
        "end_time": 1682637184576806000,
        "program": {
            "n_lines": 8,
            "program_path": "c_files/example.c"
        },
        "relations": [{
            "name": "foo",
            "variables": ["x", "y"],
            "relation":
                {"matrix": [
                    [[{"scalar": "m", "deltas": [(0, 0)]}],
                     [{"scalar": "o", "deltas": []}]],
                    [[{"scalar": "o", "deltas": []}],
                     [{"scalar": "m", "deltas": []}]]]},
            "choices": [[[0, 1], [0]]],
            "bound": {"x": "x;;", "y": "y;;x"},
            "infinity": False
        }]
    })
    mocker.patch('builtins.open')

    # load the relation
    result = load_result("whatever.txt")
    assert 'foo' in result.relations

    foo_res = result.get_func('foo')
    assert isinstance(foo_res.relation, Relation)
    assert foo_res.relation.variables == ["x", "y"]

    assert foo_res.choices.valid == [[[0, 1], [0]]]
    assert foo_res.choices.first == (0, 0)
    assert not foo_res.infinite

    # # now check that composed relation matches expectation
    first_mono = foo_res.relation.matrix[0][0].list[0]
    assert first_mono.scalar == "m"
    assert first_mono.deltas == [(0, 0)]

    # restores bound details correctly
    assert foo_res.bound.bound_dict['x'].x.vars == ["x"]
    assert foo_res.bound.bound_dict['y'].x.vars == ["y"]
    assert foo_res.bound.bound_dict['y'].z.vars == ["x"]


def test_load_relation_infty(mocker):
    """Method load infinited result correctly."""
    mocker.patch('json.load', return_value={
        "start_time": 1682639567996906000,
        "end_time": 1682639568022015000,
        "program": {
            "n_lines": 6,
            "program_path": "example.c"
        },
        "relations": [
            {
                "name": "boohoo",
                "infinity": True,
                "relation": None
            }
        ]
    })
    mocker.patch('builtins.open')

    # load the relation
    result = load_result("whatever.txt")
    assert 'boohoo' in result.relations
    bh = result.get_func('boohoo')
    assert bh is not None
    assert bh.relation is None
    assert bh.infinite


def test_read_loc(mocker):
    """Returns expected number of lines"""
    mocker.patch(
        'builtins.open',
        new_callable=mocker.mock_open,
        read_data="1\n2\n3\n4")
    result = loc("some_file.c")

    assert result == 4
