import fault
from magma_examples.gcd import GCD


def test_gcd():
    tester = fault.SynchronousTester(GCD, clock=GCD.CLK)
    tester.circuit.a = 32
    tester.circuit.b = 16
    tester.circuit.load = 1
    tester.advance_cycle()
    tester.circuit.load = 0
    tester.advance_cycle()
    tester.wait_on(tester.circuit.O1 == 1)
    tester.circuit.O0.expect(16)
    tester.compile_and_run("verilator",
                           flags=['--trace'],
                           magma_output="mlir-verilog")
