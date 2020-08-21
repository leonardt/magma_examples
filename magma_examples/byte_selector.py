import magma as m


class ByteSelector(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[32]),
        offset=m.In(m.UInt[2]),
        O=m.Out(m.UInt[8])
    )

    @m.inline_combinational()
    def select_byte():
        if io.offset == 0:
            io.O @= io.I[:8]
        elif io.offset == 1:
            io.O @= io.I[8:16]
        elif io.offset == 2:
            io.O @= io.I[16:24]
        else:
            io.O @= io.I[24:32]
