from pytest import raises
from pymwp.monomial import Monomial


def test_create_monomial_without_deltas():
    mono = Monomial('o', [])
    assert mono.scalar == 'o'
    assert mono.deltas == []


def test_create_monomial_with_duplicated_deltas():
    mono = Monomial('m', [(0, 0), (0, 0), (0, 0)])
    assert mono.scalar == 'm'
    assert mono.deltas == [(0, 0)]


def test_create_monomial_with_invalid_deltas():
    mono = Monomial('m', [(0, 2), (1, 2), (1, 1), (0, 0)])
    assert mono.scalar == 'o'
    assert mono.deltas == []


def test_monomial_product_non_empty():
    a = Monomial('m', [(0, 0)])
    b = Monomial('m', [(0, 0), (1, 1)])
    p = a * b
    assert p.scalar == 'm'
    assert p.deltas == [(0, 0), (1, 1)]


def test_monomial_product_empty_arg():
    a = Monomial('m', [(0, 0)])
    b = Monomial('o', [])
    p = a * b
    assert p.scalar == 'o'
    assert p.deltas == []


def test_monomial_product_empty_self():
    a = Monomial('o', [])
    b = Monomial('m', [(0, 0)])
    p = a * b
    assert p.scalar == 'o'
    assert p.deltas == []


def test_monomial_eval_match():
    scalar = 'm'
    mono = Monomial(scalar, [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4)])
    result = mono.eval([0, 0, 1, 1, 2])
    assert scalar == result


def test_monomial_eval_no_match():
    mono = Monomial('m', [(0, 0), (1, 1), (2, 2)])
    result = mono.eval([0, 1, 1])
    assert 'o' == result


def test_monomial_eval_longer_args_will_match():
    scalar = 'm'
    mono = Monomial(scalar, [(0, 0), (1, 1), (2, 2)])
    result = mono.eval([0, 1, 2, 3])
    assert scalar == result


def test_monomial_eval_shorter_args_will_throw():
    with raises(Exception):
        mono = Monomial('p', [(0, 0), (1, 1), (2, 2)])
        assert mono.eval([0, 1])


def test_monomial_copy():
    m = Monomial('m', [(0, 0), (1, 1)])
    n = m.copy()
    assert m.scalar == n.scalar  # same scalar
    assert m.deltas == n.deltas  # same deltas
    assert m != n  # different reference


def test_valid_insert_to_empty():
    deltas = []
    delta = (0, 0)
    deltas = Monomial.insert_delta(deltas, delta)
    assert delta in deltas
    assert deltas == [(0, 0)]


def test_valid_insert_to_nonempty():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (1, 3)
    deltas = Monomial.insert_delta(deltas, delta)
    assert delta in deltas
    assert deltas == [(0, 0), (1, 1), (2, 2), (1, 3)]


def test_insert_ignores_duplicate():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (0, 0)
    deltas = Monomial.insert_delta(deltas, delta)
    assert deltas == [(0, 0), (1, 1), (2, 2)]


def test_insert_return_empty_on_conflict():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (0, 1)
    deltas = Monomial.insert_delta(deltas, delta)
    assert deltas == []
