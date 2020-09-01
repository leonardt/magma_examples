import magma as m


class ShiftRegister(m.Circuit):
    io = m.IO(
        I=m.In(m.Bit),
        O=m.Out(m.Bit)
    ) + m.ClockIO()
    io.O @= m.fold([m.Register(m.Bit)() for _ in range(4)])(io.I)
