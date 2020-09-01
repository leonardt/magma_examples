import magma as m


PATTERN = [0, 4, 15, 14, 2, 5, 13]


class VecSearch(m.Circuit):
    io = m.IO(out=m.Out(m.UInt[4])) + m.ClockIO()
    index = m.Register(m.UInt[3], init=0)()
    index.I @= index.O + 1
    pattern = [m.UInt[4](i) for i in PATTERN]
    io.out @= m.mux(pattern, index.O)
