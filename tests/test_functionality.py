from hwtypes import BitVector

import fault
from magma_examples.functionality import Functionality, clb


def test_functionality():
    tester = fault.Tester(Functionality)
    x = BitVector.random(16)
    y = BitVector.random(16)
    tester(x, y).expect(clb(x, y, x, y))
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
