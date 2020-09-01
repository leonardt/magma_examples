import pytest
from hwtypes import BitVector
import fault

from magma_examples.simple_alu import BasicALU, SimpleALU


@pytest.mark.parametrize('circuit,ops', [
    (BasicALU, [
        lambda x, y: x,
        lambda x, y: y,
        lambda x, y: x + 1,
        lambda x, y: x - 1,
        lambda x, y: x + 4,
        lambda x, y: x - 4,
        lambda x, y: x + y,
        lambda x, y: x - y,
        lambda x, y: x < y,
        lambda x, y: x == y
    ]),
    (SimpleALU, [
        lambda x, y: x + y,
        lambda x, y: x - y,
        lambda x, y: x,
        lambda x, y: y,
    ])
])
def test_basic_alu(circuit, ops):
    tester = fault.Tester(circuit)
    tester.circuit.a = a = BitVector.random(4)
    tester.circuit.b = b = BitVector.random(4)
    for i, op in enumerate(ops):
        tester.circuit.opcode = i
        tester.eval()
        tester.circuit.out.expect(op(a, b))
    tester.compile_and_run("verilator")
