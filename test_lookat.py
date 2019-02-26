import lookat
from pytest import mark


def test_lookat__smoketest(object):
    assert lookat.format(object) is not None


def test_lookat__format(object):
    print(lookat.format(object))


def test_is_public():
    assert lookat.is_public('bla')
    assert not (lookat.is_public('_bla'))
    assert not (lookat.is_public('__bla'))


def test_doc_header(function):
    assert lookat.doc_header(function) == 'docstring of the function'


# ---------------------parse attribute---------------------


def test_parse_attribute__public_int_attribute(object):
    assert lookat.parse_attribute(object, 'number') == lookat.Attribute(
        name='number', repr="12", is_callable=False, is_public=True
    )


def test_parse_attribute__public_str_attribute(object):
    assert lookat.parse_attribute(object, 'string') == lookat.Attribute(
        name='string', repr="a piece of wood", is_callable=False, is_public=True
    )


def test_parse_attribute__public_callable(object):
    assert lookat.parse_attribute(object, 'method') == lookat.Attribute(
        name='method', repr="docstring of the method", is_callable=True, is_public=True
    )
