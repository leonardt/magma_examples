from hwtypes import BitVector
import fault

from magma_examples.log_shifter import LogShifter


def test_log_shifter():
    tester = fault.SynchronousTester(LogShifter, clock=LogShifter.CLK)
    tester.circuit.I = I = BitVector.random(16)
    tester.circuit.shift_amount = shift_amount = BitVector.random(4)
    for _ in range(3):
        tester.advance_cycle()
    tester.circuit.O.expect(I << shift_amount.zext(12))
    tester.compile_and_run("verilator")
