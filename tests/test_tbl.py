from hwtypes import BitVector
import fault

from magma_examples.tbl import Tbl


def test_tbl():
    tester = fault.Tester(Tbl)
    for _ in range(4):
        tester.circuit.addr = addr = BitVector.random(8)
        tester.eval()
        tester.circuit.out.expect(addr)
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
