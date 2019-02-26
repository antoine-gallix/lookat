from pytest import fixture


class Object:
    number = 12
    string = 'a piece of wood'
    _internal = 'detail'

    def method():
        """docstring of the method

        some more details
        """

        pass

    def _private_method():
        """docstring of the private method

        private details
        """
        pass


def a_function():
    """docstring of the function

    some more details
    """


@fixture
def object():
    return Object()


@fixture
def function():
    return a_function
