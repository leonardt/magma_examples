import random

import pytest

from magma_examples.adder import Adder
import fault as f
from hwtypes import BitVector


@pytest.mark.parametrize("N", [random.randint(1, 16) for _ in range(4)])
def test_adder4(N):
    N = random.randint(1, 16)
    tester = f.Tester(Adder(N))
    tester.circuit.A = A = BitVector.random(N)
    tester.circuit.B = B = BitVector.random(N)
    tester.circuit.CIN = CIN = BitVector.random(1)
    tester.eval()
    tester.circuit.SUM.expect(A + B + CIN.zext(N - 1), msg=f"N={N}")
    tester.circuit.COUT.expect((A.zext(1) + B.zext(1) +
                                CIN.zext(N))[-1])
    tester.compile_and_run("verilator")
