import random
import tempfile

import pytest

from magma_examples.adder import Adder
import fault as f
from hwtypes import BitVector


@pytest.mark.parametrize("N", [random.randint(1, 16) for _ in range(4)])
def test_adder(N):
    tester = f.Tester(Adder(N))
    tester.circuit.A = A = BitVector.random(N)
    tester.circuit.B = B = BitVector.random(N)
    tester.circuit.CIN = CIN = BitVector.random(1)
    tester.eval()
    tester.circuit.SUM.expect(A + B + CIN.zext(N - 1))
    tester.circuit.COUT.expect((A.zext(1) + B.zext(1) +
                                CIN.zext(N))[-1])
    with tempfile.TemporaryDirectory() as dir_:
        tester.compile_and_run("verilator", directory=dir_,
                               magma_output="mlir-verilog")
