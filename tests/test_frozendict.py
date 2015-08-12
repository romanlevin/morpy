from morpy.frozendict import frozendict
from pytest import raises


def test_cant_set_item():
    d = frozendict({'a': 'a'})
    with raises(TypeError):
        d['b'] = 'b'
    assert 'b' not in d


def test_repr():
    d = frozendict({'a': 'a'})
    assert str(d) == "<frozendict {'a': 'a'}>"


def test_copy():
    d = frozendict({'a': 'a'})
    d2 = d.copy()
    assert d is not d2
