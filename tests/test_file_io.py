from pymwp.file_io import default_file_out #, save_relation, load_relation
from pymwp.relation import Relation


def test_file_out_name_wo_path():
    input_file = "my_c_file.c"
    out_file = default_file_out(input_file)

    assert out_file == "output/my_c_file.txt"


def test_file_out_name_with_path():
    input_file = "my_dir/of/files/example.c"
    out_file = default_file_out(input_file)

    assert out_file == "output/example.txt"


def test_save_relation():
    filename = 'output.txt'
    relation = Relation(['X1', 'X2', 'X3'])
    combinations = [[2, 0, 0], [1, 0, 0]]
    # save_relation(filename, relation, combinations)
    # TODO: need to mock file open...
    pass
