import fault

from magma_examples.risc import Risc


def test_risc():
    tester = fault.SynchronousTester(Risc, Risc.CLK)

    def write(addr, data):
        tester.circuit.is_write = 1
        tester.circuit.write_addr = addr
        tester.circuit.write_data = data
        tester.advance_cycle()

    def boot():
        tester.circuit.is_write = 0
        tester.circuit.boot = 1
        tester.advance_cycle()

    def I(op, rc, ra, rb):
        return (op << 24) | (rc << 16) | (ra << 8) | rb

    app = [
        I(1, 1, 0, 1),  # r1 <- 1
        I(0, 1, 1, 1),  # r1 <- r1 + r1
        I(0, 1, 1, 1),  # r1 <- r1 + r1
        I(0, 255, 1, 0),  # rh <- r1
    ]
    write(0, 0)
    for addr, instr in enumerate(app):
        write(addr, instr)
    boot()
    tester.circuit.boot = 0
    tester.wait_until_high(tester.circuit.valid)
    tester.circuit.out.expect(4)
    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           magma_opts={"flatten_all_tuples": True},
                           flags=["-Wno-WIDTH", "-Wno-UNUSED", "-Wno-LATCH"])
