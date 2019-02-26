from collections import namedtuple
import string
from dataclasses import dataclass
from itertools import chain


@dataclass
class Attribute:
    name: str
    is_callable: bool
    is_public: bool
    repr: str = ""


def doc_header(o):
    try:
        return o.__doc__.split('\n')[0]
    except (AttributeError):
        return None


def is_public(s):
    return not (s.startswith('_'))


def parse_attribute(object, attribute_name):
    value = getattr(object, attribute_name)
    attribute = Attribute(
        name=attribute_name,
        is_public=is_public(attribute_name),
        is_callable=callable(value),
    )
    if attribute.is_callable:
        attribute.repr = doc_header(value)
    else:
        attribute.repr = str(value)
    return attribute


def parse_attributes(object):
    attribute_names = dir(object)
    public_attribute_names = filter(is_public, attribute_names)
    return (parse_attribute(object, name) for name in public_attribute_names)


def format_attribute(attribute):
    return f'{attribute.name}{"()" if attribute.is_callable else ""}'


def title_line(object):
    return str(type(object))


def order_attributes(attributes):
    simple_attributes = [attr for attr in attributes if not (attr.is_callable)]
    private_attributes = [attr for attr in simple_attributes if not (attr.is_public)]
    public_attributes = [attr for attr in simple_attributes if attr.is_public]

    methods = [attr for attr in attributes if attr.is_callable]
    private_methods = [attr for attr in methods if not (attr.is_public)]
    public_methods = [attr for attr in methods if attr.is_public]

    return private_attributes + public_attributes + private_methods + public_methods


def attribute_lines(object, all=False):
    attributes = parse_attributes(object)
    ordered_attributes = order_attributes(attributes)
    return map(format_attribute, ordered_attributes)


def format(object, **kwargs):
    lines = []
    lines.append(title_line(object, **kwargs))
    lines.append('')
    lines.extend(attribute_lines(object, **kwargs))
    return '\n'.join(lines)


def lookat(object):
    print(format(object))
