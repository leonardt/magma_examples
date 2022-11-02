import fault
from hwtypes import BitVector
from magma_examples.enable_shift_register import EnableShiftRegister


def test_enable_shift_register():
    print(repr(EnableShiftRegister))
    tester = fault.SynchronousTester(EnableShiftRegister,
                                     EnableShiftRegister.CLK)
    input_seq = [BitVector.random(4) for _ in range(8)]
    output_seq = [0 for _ in range(3)] + input_seq[:5]
    tester.circuit.shift = True
    for I, O in zip(input_seq, output_seq):
        tester.circuit.I = I
        tester.advance_cycle()
        tester.circuit.O.expect(O)
    tester.circuit.shift = False
    for _ in range(4):
        tester.circuit.I = BitVector.random(4)
        tester.advance_cycle()
        tester.circuit.O.expect(input_seq[4])
    tester.circuit.ASYNCRESET = 1
    tester.advance_cycle()
    tester.circuit.ASYNCRESET = 0
    tester.circuit.O.expect(0)
    tester.advance_cycle()
    tester.circuit.O.expect(0)
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
