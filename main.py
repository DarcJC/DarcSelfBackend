#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer
import uvicorn


main = typer.Typer()


@main.command()
def dev():
    uvicorn.run('core:app', reload=True, port=5000)


@main.command()
def about():
    typer.echo("Powerd by magic DarcJC.")


if __name__ == '__main__':
    main()
