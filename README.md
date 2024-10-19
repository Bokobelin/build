# Build
A new build system.

An example buildfile and how to run it:
```
say = echo

init():
    @echo off

hello(init):
    $(say) hello world

run(hello):
    $(say) hi!
```
To run use `python src/main.py path_to_your_buildfile run`.
