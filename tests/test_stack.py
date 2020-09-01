from hwtypes import BitVector
import fault

from magma_examples.stack import Stack


def push(tester, data):
    tester.circuit.en = 1
    tester.circuit.data_in = data
    tester.circuit.push = 1
    tester.advance_cycle()
    tester.circuit.en = 0
    tester.circuit.data_in = 0
    tester.circuit.push = 0


def expect_pop(tester, data):
    tester.circuit.en = 1
    tester.circuit.pop = 1
    tester.advance_cycle()
    tester.circuit.en = 0
    tester.circuit.pop = 0
    tester.circuit.data_out.expect(data)


def push_and_pop(tester, data):
    tester.circuit.en = 1
    tester.circuit.data_in = data
    tester.circuit.push = 1
    tester.circuit.pop = 1
    tester.advance_cycle()
    tester.circuit.en = 0
    tester.circuit.data_in = 0
    tester.circuit.push = 0
    tester.circuit.pop = 0


def test_stack():
    Stack4 = Stack(4)
    tester = fault.SynchronousTester(Stack4, Stack4.CLK)
    push(tester, 3)
    push(tester, 1)
    push(tester, 2)
    push(tester, 0)
    expect_pop(tester, 0)
    expect_pop(tester, 2)
    expect_pop(tester, 1)
    expect_pop(tester, 3)

    # Extra pops shouldn't change value
    expect_pop(tester, 3)
    expect_pop(tester, 3)

    push(tester, 3)

    # pushing and popping should only push
    push_and_pop(tester, 2)
    push_and_pop(tester, 3)
    expect_pop(tester, 3)
    expect_pop(tester, 2)
    expect_pop(tester, 3)

    # pushing more than depth will be ignored
    push(tester, 0)
    push(tester, 1)
    push(tester, 2)
    push(tester, 3)
    push(tester, 4)
    expect_pop(tester, 3)
    expect_pop(tester, 2)
    expect_pop(tester, 1)
    expect_pop(tester, 0)

    tester.compile_and_run("verilator")
