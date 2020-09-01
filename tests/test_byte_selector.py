from hwtypes import BitVector
import fault

from magma_examples.byte_selector import ByteSelector


def test_byte_selector():
    tester = fault.Tester(ByteSelector)
    tester.circuit.I = I = BitVector.random(32)
    for i in range(4):
        tester.circuit.offset = i
        tester.eval()
        tester.circuit.O.expect(I[i * 8:(i + 1) * 8])
    tester.compile_and_run("verilator")
