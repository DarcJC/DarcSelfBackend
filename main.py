#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

import typer
import uvicorn

main = typer.Typer()


@main.command("dev", help='Run a development server')
def dev():
    import os
    os.environ.setdefault('DEBUG', 'True')
    uvicorn.run('core:app', reload=True, port=5000)


@main.command("about", help='About DarcSelf')
def about():
    typer.echo("Powerd by magic DarcJC.")


@main.command("start", help='Run in production')
def start(
        *,
        host: Optional[str] = '127.0.0.1',
        port: Optional[int] = 5000,
        workers: Optional[int] = 4,
):
    uvicorn.run('core:app', reload=False, port=port, host=host, workers=workers)


if __name__ == '__main__':
    main()
