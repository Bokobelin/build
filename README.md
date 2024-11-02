# Build

# This repository is no longer maintained. An up-to-date version can be found at https://github.com/Corevia/build

A new build system.

An example buildfile and how to run it:
```
say = echo

private init():
    @echo off

private hello(init):
    $(say) hello world

run(hello):
    $(say) hi!
```
To run use `python src/main.py path_to_your_buildfile run`.
