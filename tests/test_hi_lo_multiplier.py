from hwtypes import BitVector
import fault

from magma_examples.hi_lo_multiplier import HiLoMultiplier


def test_hi_lo_multiplier():
    tester = fault.Tester(HiLoMultiplier)
    tester.circuit.A = A = BitVector.random(16)
    tester.circuit.B = B = BitVector.random(16)
    tester.eval()
    C = A.zext(16) * B.zext(16)
    tester.circuit.Lo.expect(C[:16])
    tester.circuit.Hi.expect(C[16:])
    tester.compile_and_run("verilator")

