import magma as m
from ast_tools.passes import loop_unroll
from ast_tools.macros import unroll


class EnableShiftRegister(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[4]),
        shift=m.In(m.Enable),
        O=m.Out(m.UInt[4])
    ) + m.ClockIO(has_async_reset=True)
    regs = [m.Register(m.UInt[4], reset_type=m.AsyncReset, has_enable=True)()
            for _ in range(4)]

    with m.when(io.shift):
        regs[0].I @= io.I
        for i in range(3):
            regs[i + 1].I @= regs[i].O

    io.O @= regs[-1].O
