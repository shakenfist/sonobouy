from collections import defaultdict


ASSERTIONS_BY_DEPENDENCY = defaultdict(list)


class AssertionBase(object):
    internal_name = 'unknown'
    pretty_name = 'unknown'
    depends_on = []

    def execute(self):
        ...


def register(obj):
    global ASSERTIONS_BY_DEPENDENCY

    if not obj.depends_on:
        ASSERTIONS_BY_DEPENDENCY[None].append(obj)
    else:
        for dep in obj.depends_on:
            ASSERTIONS_BY_DEPENDENCY[dep].append(obj)
