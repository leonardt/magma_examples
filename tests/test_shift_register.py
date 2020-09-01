import fault

from magma_examples.shift_register import ShiftRegister


def test_shift_register():
    tester = fault.SynchronousTester(ShiftRegister, clock=ShiftRegister.CLK)
    seq = [0, 1, 1, 0, 1, 0, 0, 1]
    delay = [0, 0, 0]
    in_seq, out_seq = seq + delay, delay + seq
    for i, o in zip(in_seq, out_seq):
        tester.circuit.I = i
        tester.advance_cycle()
        tester.circuit.O.expect(o)
    tester.compile_and_run("verilator")
