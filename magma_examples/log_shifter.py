import magma as m


class LogShifter(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[16]),
        shift_amount=m.In(m.UInt[4]),
        O=m.Out(m.UInt[16])
    ) + m.ClockIO()
    s0 = m.Register(m.UInt[16])()
    s1 = m.Register(m.UInt[16])()
    s2 = m.Register(m.UInt[16])()
    @m.inline_combinational()
    def logic():
        if io.shift_amount[3] == 1:
            s0.I @= io.I << 8
        else:
            s0.I @= io.I

        if io.shift_amount[2] == 1:
            s1.I @= s0.O << 4
        else:
            s1.I @= s0.O

        if io.shift_amount[1] == 1:
            s2.I @= s1.O << 2
        else:
            s2.I @= s1.O

        if io.shift_amount[0] == 1:
            io.O @= s2.O << 1
        else:
            io.O @= s2.O
