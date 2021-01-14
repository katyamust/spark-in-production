#!/bin/sh -l

cd ./src/python/src
python setup.py install
pytest tests
