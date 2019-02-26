import logging
from collections import namedtuple
from inspect import ismodule

from sqlalchemy import inspect

Attribute = namedtuple('Attribute', ['name', 'repr'])
Attribute_Group = namedtuple('Attribute_Group', ['attributes', 'name'])


def doc_header(o):
    try:
        return o.__doc__.split('\n')[0]
    except (AttributeError):
        return None


def type_info(o):
    type_ = type(o)
    base_types = [int, bool, type(None), dict, frozenset, str, list, tuple]
    if type_ in base_types:
        return ''
    else:
        return str(type_)


def truncated_str(x):
    max_len = 40
    truncated_len = 20
    s = str(x)
    s_len = len(s)
    if s_len > max_len:
        return f'{s[:truncated_len]}...      ({s_len})'
    else:
        return s


class Object_Viewer:
    def __init__(self, o, printer=print):
        self.o = o
        self.print = printer

    def view(self):
        self.print_title()
        attributes = self.get_attributes_names()
        self.set_column_width(attributes)
        groups = self.resolve_attributes(attributes)
        for group in groups:
            self.view_group(group)

    def get_attributes_names(self):
        return [a for a in dir(self.o) if self.is_viewed(a)]

    def get_attribute(self, a):
        try:
            return getattr(self.o, a)
        except (TypeError, AttributeError, ValueError):
            return None

    def resolve_attributes(self, attributes_names):
        """split attributes into groups"""

        callables = Attribute_Group(attributes=[], name='callables')
        properties = Attribute_Group(attributes=[], name='properties')
        modules = Attribute_Group(attributes=[], name='modules')
        errors = Attribute_Group(attributes=[], name='errors')

        for name in attributes_names:
            try:
                value = getattr(self.o, name)
            except:
                errors.attributes.append(Attribute(name=name, repr='<error>'))
            if callable(value):
                callables.attributes.append(
                    Attribute(name=f'{name}()', repr=doc_header(value))
                )
            elif ismodule(value):
                modules.attributes.append(Attribute(name=name, repr=str(value)))
            else:
                properties.attributes.append(
                    Attribute(
                        name=name, repr=f'{truncated_str(value)} {type_info(value)}'
                    )
                )
        return [modules, properties, callables, errors]

    def print_attribute(self, attribute):
        self.print(f'{attribute.name:{self.first_column_width}} : {attribute.repr}')

    def view_group(self, group):
        if not group.attributes:
            return
        self.print_group_title(group)
        for a in group.attributes:
            self.print_attribute(a)

    def is_viewed(self, a):
        return not a[0] == '_'

    # -------------------printers-----------------------

    def set_column_width(self, attributes):
        self.first_column_width = max([len(name) for name in attributes])

    def print_title(self):
        self.print(f'type : {type(self.o)}')

    def print_group_title(self, group):
        if group.name:
            self.print(f'\n---| {group.name}\n')


def format_logger(l):
    info = []
    info.append(f'logger : {l.name}({logging.getLevelName(l.level)})')
    if l.propagate:
        info.append(f'propagate to : {l.parent!r}')
    else:
        info.append('no propagation')
    for handler in l.handlers:
        info.append(f'handler : {handler.__class__.__name__}')
    return '\n'.join(info)


def view_model(model):
    mapper = inspect(model)
    print(mapper.class_)
    print()
    print('---| relationships')
    for r in mapper.relationships.keys():
        print(r)
    print()
    print('---| properties')
    for p in mapper.column_attrs:
        print(f'{p.key}')


# -----------------------------------------------


def view(o, **kwargs):
    if isinstance(o, logging.Logger):
        print(format_logger(o))
    else:
        viewer = Object_Viewer(o, **kwargs)
        viewer.view()
