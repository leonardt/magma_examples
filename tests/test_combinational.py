import fault
from hwtypes import BitVector
from magma_examples.combinational import add


def test_combinational():
    tester = fault.Tester(add)
    x = BitVector.random(16)
    y = BitVector.random(16)
    tester(x, y).expect(x + y)
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
