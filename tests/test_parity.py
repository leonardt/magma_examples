import fault
import random

from magma_examples.parity import Parity


def test_parity():
    tester = fault.SynchronousTester(Parity, Parity.CLK)
    is_odd = 0
    for _ in range(10):
        bit = random.getrandbits(1)
        tester.circuit.I = bit
        tester.advance_cycle()
        is_odd = (is_odd + bit) % 2
        tester.circuit.O.expect(is_odd)
    tester.compile_and_run("verilator")

