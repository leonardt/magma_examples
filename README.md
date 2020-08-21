# magma_examples
![Linux Test](https://github.com/leonardt/magma_examples/workflows/Linux%20Test/badge.svg)

magma port of https://github.com/ucb-bar/chisel-tutorial

Currently WIP, please post any questions on GitHub Issues or feel free to
contribute!

Example magma designs can be found in [magma_examples](./magma_examples), the
corresponding unit tests can be found in [tests](./tests).

This repository also serves an example for setting up a magma repo for CI with
GitHub actions.

Please use GitHub Issues to post any questions about the examples.

## Dependencies
### Ubuntu
```
sudo apt install verilator libgmp-dev libmpfr-dev libmpc-dev
```
### MacOS
```
brew install verilator gmp mpfr libmpc
```

## Test
```
pip install pytest
pip install -e .
pytest tests
```

