# Copyright 2024 Michael Still

import click
import copy

from sonobouy import assertions_base
from sonobouy.assertions import packages_dnf


@click.group()
@click.pass_context
def cli(ctx):
    if not ctx.obj:
        ctx.obj = {}


@cli.command(name='run', help='Perform an sonobouy analysis, one ping!')
@click.pass_context
def run(ctx):
    runnable = copy.copy(assertions_base.ASSERTIONS_BY_DEPENDENCY[None])

    while runnable:
        a = runnable.pop(0)
        result = a.execute()
        print(f'{a.pretty_name}: {result}')
        if result:
            for obj in assertions_base.ASSERTIONS_BY_DEPENDENCY[a.internal_name]:
                obj.depends_on.remove(a.internal_name)
                if not obj.depends_on:
                    runnable.append(obj)
            del assertions_base.ASSERTIONS_BY_DEPENDENCY[a.internal_name]

    unrunnable = []
    for dep in assertions_base.ASSERTIONS_BY_DEPENDENCY:
        for a in assertions_base.ASSERTIONS_BY_DEPENDENCY[dep]:
            if a.depends_on:
                if a.internal_name not in unrunnable:
                    unrunnable.append(a.internal_name)
    print()
    print(f'All runnable assertions executed ({len(unrunnable)} not '
          'executable)')


cli.add_command(run)
