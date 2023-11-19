import os
import pathlib

statics = (
    str(
        pathlib.Path(__file__)
        .parent.resolve()
        .parent.resolve()
        .parent.resolve()
    )
    + '/statics/'
)

if not os.path.exists(statics):
    os.mkdir(statics)
