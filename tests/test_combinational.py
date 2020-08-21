import fault
from hwtypes import BitVector
from magma_examples.combinational import Combinational


def test_combinational():
    tester = fault.Tester(Combinational)
    tester.circuit.x = x = BitVector.random(16)
    tester.circuit.y = y = BitVector.random(16)
    tester.eval()
    tester.circuit.z.expect(x + y)
    tester.compile_and_run("verilator")
