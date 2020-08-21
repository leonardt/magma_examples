import fault
from hwtypes import BitVector
from magma_examples.darken import Darken


def test_darken():
    tester = fault.Tester(Darken)
    tester.circuit.I = I = BitVector.random(8)
    tester.eval()
    tester.circuit.O.expect(I << 1)
