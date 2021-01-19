#!/bin/sh -l

cd ./src/python/src
python setup.py install
cd ../tests/
ls
pytest unit-tests
