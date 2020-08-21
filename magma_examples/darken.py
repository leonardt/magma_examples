import magma as m


class Darken(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[8]),
        O=m.Out(m.UInt[8])
    )
    io.O @= io.I << 1
