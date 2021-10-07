import os
import json

from pymwp.file_io import default_file_out, save_relation, load_relation
from pymwp import Relation


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


def test_save_relation(mocker):
    """Method generates directory when it does not exist then saves."""
    # mock all built-ins
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    mocker.patch('builtins.open')
    mocker.patch('json.dump')

    filename = 'fake_path/deep/path/output.txt'
    save_relation(filename, {'foo': (Relation(), [[]], False)})

    # it creates directory path when dir/s do not exist
    os.makedirs.assert_called_once_with('fake_path/deep/path')
    # it saves json
    json.dump.assert_called_once()


def test_load_relation(mocker):
    """Method generates expected object instance."""
    # mock built-ins
    mocker.patch('json.load', return_value={
        "foo": {
            "relation": {"variables": ["x", "y"],
                         "matrix": [
                             [[{"scalar": "m", "deltas": [(0, 0)]}],
                              [{"scalar": "o", "deltas": []}]],
                             [[{"scalar": "o", "deltas": []}],
                              [{"scalar": "o", "deltas": []}]]]},
            "choices": [[0, 0, 0], [1, 0, 0]],
            "infinity": False
        }
    })
    mocker.patch('builtins.open')

    # load the relation
    result = load_relation("whatever.txt")
    assert 'foo' in result

    (relation, combinations, infinity) = result["foo"]
    assert isinstance(relation, Relation)

    first_poly = relation.matrix[0][0].list[0]

    # # now check that composed relation matches expectation
    assert combinations == [[0, 0, 0], [1, 0, 0]]
    assert relation.variables == ["x", "y"]
    assert first_poly.scalar == "m"
    assert first_poly.deltas == [(0, 0)]
    assert not infinity
