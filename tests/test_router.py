from hwtypes import BitVector
import fault


from magma_examples.router import Router


def test_router():
    DefaultRouter = Router()
    tester = fault.Tester(DefaultRouter, DefaultRouter.CLK)

    def read_routing_table(addr, data):
        tester.circuit.read_routing_table_request.addr = addr
        tester.circuit.read_routing_table_request.valid = 1
        tester.circuit.read_routing_table_response.ready = 1
        tester.step()
        tester.circuit.read_routing_table_request.ready.expect(1)
        tester.circuit.read_routing_table_response.valid.expect(1)
        tester.step()
        tester.circuit.read_routing_table_request.valid = 0
        tester.circuit.read_routing_table_response.ready = 0
        tester.circuit.read_routing_table_response.data.expect(data)

    def write_routing_table(addr, data):
        tester.circuit.load_routing_table_request.addr = addr
        tester.circuit.load_routing_table_request.data = data
        tester.circuit.load_routing_table_request.valid = 1
        tester.step()
        tester.circuit.load_routing_table_request.ready.expect(1)
        tester.step()
        tester.circuit.load_routing_table_request.valid = 0

    def write_routing_table_with_confirm(addr, data):
        write_routing_table(addr, data)
        read_routing_table(addr, data)

    def route_packet(header, body, routed_to):
        tester.circuit.I.header = header
        tester.circuit.I.body = body
        tester.circuit.I.valid = 1
        tester.circuit.O[routed_to].ready = 1
        tester.step()

        tester.circuit.I.ready.expect(1)
        tester.circuit.O[routed_to].valid.expect(1)
        tester.step()

        tester.circuit.I.valid = 0
        tester.circuit.O[routed_to].ready = 0
        tester.circuit.O[routed_to].body.expect(body)

    read_routing_table(0, 0)

    # load routing table, confirm each write as built
    for i in range(4):
        write_routing_table_with_confirm(i, (i + 1) % 4)

    # check them in reverse order just for fun
    for i in range(3, -1, -1):
        read_routing_table(i, (i + 1) % 4)

    # send some regular packets
    for i in range(4):
        route_packet(i, i * 3, (i + 1) % 4)

    # generate a new routing table
    new_routing_table = [int(BitVector.random(2)) for _ in range(15)]
    print(new_routing_table)

    # load a new routing table
    for i, destination in enumerate(new_routing_table):
        write_routing_table(i, destination)

    # send a bunch of packets, with random values
    for i in range(20):
        data = BitVector.random(64)
        print(new_routing_table[i % 15])
        print(type(DefaultRouter.O))
        route_packet(i % 15, data, new_routing_table[i % 15])

    tester.compile_and_run("verilator",
                           magma_output="mlir-verilog",
                           flags=['--trace', '-Wno-UNUSED'])
