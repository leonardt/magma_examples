import magma as m
from ast_tools.passes import loop_unroll
from ast_tools.macros import unroll


class Router(m.Generator2):
    def __init__(
        self,
        addr_width=32,
        data_width=64,
        header_width=8,
        route_table_size=15,
        num_outputs=4):

        class ReadCmd(m.Product):
            addr = m.In(m.UInt[addr_width])
            ready = m.Out(m.Bit)
            valid = m.In(m.Bit)

        class ReadResp(m.Product):
            data = m.Out(m.UInt[addr_width])
            ready = m.In(m.Bit)
            valid = m.Out(m.Bit)

        class WriteCmd(m.Product):
            data = m.In(m.UInt[addr_width])
            addr = m.In(m.UInt[addr_width])
            ready = m.Out(m.Bit)
            valid = m.In(m.Bit)

        class Packet(m.Product):
            header = m.In(m.UInt[header_width])
            body = m.In(m.UInt[data_width])
            ready = m.Out(m.Bit)
            valid = m.In(m.Bit)

        self.io = io = m.IO(
            read_routing_table_request=ReadCmd,
            read_routing_table_response=ReadResp,
            load_routing_table_request=WriteCmd,
            I=Packet,
            O=m.Array[num_outputs, m.Flip(Packet)]
        ) + m.ClockIO()

        entry_size = max((num_outputs - 1).bit_length(), 1)
        tbl = m.Memory(route_table_size, m.UInt[entry_size])()
        read_resp_valid = (io.read_routing_table_request.valid &
                           io.read_routing_table_response.ready)
        io.read_routing_table_response.valid @= read_resp_valid
        io.read_routing_table_response.data @= m.zext(tbl.RDATA,
                                                      addr_width - entry_size)

        tbl.WDATA @= io.load_routing_table_request.data[:entry_size]
        io.load_routing_table_request.data[entry_size:].unused()
        io.load_routing_table_request.addr[entry_size:].unused()

        tbl_addr_width = m.bitutils.clog2(route_table_size)
        tbl.WADDR @= io.load_routing_table_request.addr[:tbl_addr_width]

        tbl.WE @= ~read_resp_valid & io.load_routing_table_request.valid
        io.read_routing_table_request.ready @= read_resp_valid
        tbl.RADDR @= m.mux(
            [
                io.I.header[:tbl_addr_width],
                io.read_routing_table_request.addr[:tbl_addr_width]
            ], read_resp_valid
        )
        io.read_routing_table_request.addr[tbl_addr_width:].unused()

        idx = tbl.RDATA
        io.load_routing_table_request.ready @= (~read_resp_valid &
                                                io.load_routing_table_request.valid)
        I_ready = (~read_resp_valid & ~io.load_routing_table_request.valid &
                   m.mux([o.ready for o in io.O], idx))
        io.I.ready @= I_ready
        for i in range(num_outputs):
            io.O[i].valid @= (idx == i) & I_ready & io.I.valid
            io.O[i].header @= io.I.header
            io.O[i].body @= io.I.body
