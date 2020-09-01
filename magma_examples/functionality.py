import magma as m


@m.combinational2()
def clb(a: m.UInt[16], b: m.UInt[16], c: m.UInt[16],
        d: m.UInt[16]) -> m.UInt[16]:
    return (a & b) | (~c & d)


class Functionality(m.Circuit):
    io = m.IO(
        x=m.In(m.UInt[16]),
        y=m.In(m.UInt[16]),
        z=m.Out(m.UInt[16]),
    )
    io.z @= clb(io.x, io.y, io.x, io.y)
