# magma-riscv-mini
![Linux Test](https://github.com/leonardt/magma_examples/workflows/Linux%20Test/badge.svg)

magma port of https://github.com/ucb-bar/chisel-tutorial

Currently WIP, please post any questions on GitHub Issues or feel free to
contribute!

## Examples
* [full_adder.py](magma_examples/full_adder.py), [test_full_adder.py](tests/test_full_adder.py)
* [adder4.py](magma_examples/adder4.py), [test_adder4.py](tests/test_adder4.py)
* [adder.py](magma_examples/adder.py), [test_adder.py](tests/test_adder.py)

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

