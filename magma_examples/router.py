import magma as m


class Router(m.Generator2):
    def __init__(
        self,
        addr_width=32,
        data_width=64,
        header_width=8,
        route_table_size=15,
        num_outputs=4
    ):

        class ReadCmd(m.Product):
            addr = m.UInt[addr_width]

        class WriteCmd(m.Product):
            data = m.UInt[addr_width]
            addr = m.UInt[addr_width]

        class Packet(m.Product):
            header = m.UInt[header_width]
            body = m.UInt[data_width]

        self.io = io = m.IO(
            read_routing_table_request=m.DeqIO[ReadCmd],
            read_routing_table_response=m.EnqIO[m.UInt[addr_width]],
            load_routing_table_request=m.DeqIO[WriteCmd],
            I=m.DeqIO[Packet],
            O=m.Array[num_outputs, m.EnqIO[Packet]]
        ) + m.ClockIO()

        entry_size = max((num_outputs - 1).bit_length(), 1)
        tbl = m.Memory(route_table_size, m.UInt[entry_size])()
        io.read_routing_table_request.no_deq()
        io.load_routing_table_request.no_deq()
        io.read_routing_table_response.no_enq()

        io.I.no_deq()
        for elem in io.O:
            # TODO: no deq/enq for tuple type
            # elem.no_enq()
            elem.valid @= 0
            elem.data @= Packet(0, 0)

        tbl_addr_width = m.bitutils.clog2safe(route_table_size)

        with m.when(io.read_routing_table_request.valid &
                    io.read_routing_table_response.ready):
            io.read_routing_table_response.data[:entry_size] @= \
                tbl[io.read_routing_table_request.deq().addr[
                    :tbl_addr_width
                ]]
            io.read_routing_table_response.data[entry_size:] @= 0
            io.read_routing_table_response.valid @= 1
            # TODO: staged memory port zext bug
            # io.read_routing_table_response.enq(
            #     tbl[io.read_routing_table_request.deq().addr])
        with m.elsewhen(io.load_routing_table_request.valid):
            cmd = io.load_routing_table_request.deq()
            tbl[cmd.addr[:tbl_addr_width]] @= cmd.data[:entry_size]
        with m.elsewhen(io.I.valid):
            pkt = io.I.data
            idx = tbl[pkt.header[:m.bitutils.clog2safe(route_table_size)]]
            # TODO: support dynamic access to mixed array
            # with m.when(io.O[idx].ready):
            #     io.I.deq()
            #     io.O[idx].enq(pkt)
            for i, elem in enumerate(io.O):
                with m.when(io.O[i].ready & (idx == i)):
                    io.I.deq()
                    elem.enq(pkt)
