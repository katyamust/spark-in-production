#!/bin/sh -l

cd ./src/python/src
python setup.py install
cd ../../../tests/
pytest unit-tests
