import magma as m


class Combinational(m.Circuit):
    io = m.IO(
        x=m.In(m.UInt[16]),
        y=m.In(m.UInt[16]),
        z=m.Out(m.UInt[16])
    )
    io.z @= io.x + io.y
