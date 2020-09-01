import magma as m


class Tbl(m.Circuit):
    io = m.IO(addr=m.In(m.UInt[8]), out=m.Out(m.UInt[8]))
    init = tuple(m.UInt[8](i) for i in range(256))
    lut = m.LUT(m.UInt[8], init)()
    io.out @= lut(io.addr)
