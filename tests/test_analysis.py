from pytest import raises
from pymwp.analysis import Analysis
from .sample_ast import EMPTY_MAIN, INFINITE_2C


def test_analyze_empty_file(mocker):
    # here we mock the pycparser - the unit test is not about testing
    # the functionality of the parser, instead what happens on different
    # files it returns
    mocker.patch('pymwp.analysis.Analysis.parse_c_file', return_value=None)
    # should return non-zero exit
    with raises(SystemExit):
        Analysis.run('empty input')


def test_analyze_empty_main(mocker):
    mocker.patch('pymwp.analysis.Analysis.parse_c_file',
                 return_value=EMPTY_MAIN)

    with raises(SystemExit):
        # should return non-zero exit
        Analysis.run('empty main')


def test_analyze_simple_infinite(mocker):
    mocker.patch('pymwp.analysis.Analysis.parse_c_file',
                 return_value=INFINITE_2C)

    relation, combinations = Analysis.run("infinite_2.c", no_save=True)

    assert combinations == []  # no combinations since it is infinite
    assert relation.variables == ['X0', 'X1']  # expected variables
    assert str(relation.matrix[0][0].list[0]) == 'm'
    assert str(relation.matrix[0][0].list[1]) == 'i.delta(0,0)'
    assert str(relation.matrix[0][0].list[2]) == 'i.delta(0,0).delta(0,1)'
    assert str(relation.matrix[0][0].list[3]) == 'i.delta(0,0).delta(1,1)'
