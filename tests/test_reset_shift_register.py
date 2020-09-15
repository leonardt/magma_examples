import fault

from magma_examples.reset_shift_register import ResetShiftRegister


def test_reset_shift_register():
    tester = fault.SynchronousTester(ResetShiftRegister,
                                     clock=ResetShiftRegister.CLK)
    tester.circuit.RESETN = 1
    seq = [0, 1, 1, 0, 1, 0, 0, 1]
    delay = [0, 0, 0]
    in_seq, out_seq = seq + delay, delay + seq
    tester.circuit.shift = 1
    for i, o in zip(in_seq, out_seq):
        tester.circuit.I = i
        tester.advance_cycle()
        tester.circuit.O.expect(o)
    tester.circuit.shift = 0
    tester.circuit.I = 1
    for i in range(4):
        tester.advance_cycle()
        tester.circuit.O.expect(1)
    tester.circuit.RESETN = 1
    tester.advance_cycle()
    tester.circuit.RESETN = 0
    tester.advance_cycle()
    tester.circuit.RESETN = 1
    tester.circuit.shift = 1
    for i in range(3):
        tester.advance_cycle()
        tester.circuit.O.expect(0)
    tester.compile_and_run("verilator")
