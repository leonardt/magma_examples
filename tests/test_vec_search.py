import fault

from magma_examples.vec_search import VecSearch, PATTERN


def test_vec_search():
    tester = fault.SynchronousTester(VecSearch, clock=VecSearch.CLK)
    for item in PATTERN:
        tester.circuit.out.expect(item)
        tester.advance_cycle()
    tester.compile_and_run("verilator", magma_opts={"verilator_compat": True})
