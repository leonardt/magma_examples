import magma as m


class ResetShiftRegister(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[4]),
        shift=m.In(m.Enable),
        O=m.Out(m.UInt[4])
    ) + m.ClockIO(has_resetn=True)
    regs = [m.Register(m.UInt[4], has_enable=True, reset_type=m.ResetN)()
            for _ in range(4)]
    io.O @= m.fold(regs, foldargs={"I": "O"},
                   forkargs={"CE"})(io.I, CE=io.shift, RESETN=io.RESETN)
