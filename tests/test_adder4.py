from magma_examples.adder4 import Adder4
import fault as f
from hwtypes import BitVector


def test_adder4():
    tester = f.Tester(Adder4)
    for _ in range(4):
        tester.circuit.A = A = BitVector.random(4)
        tester.circuit.B = B = BitVector.random(4)
        tester.circuit.CIN = CIN = BitVector.random(1)
        tester.eval()
        tester.circuit.SUM.expect(A + B + CIN.zext(3))
        tester.circuit.COUT.expect((A.zext(1) + B.zext(1) + CIN.zext(4))[-1])
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
