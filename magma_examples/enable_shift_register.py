import magma as m
from ast_tools.passes import loop_unroll
from ast_tools.macros import unroll


# Depends on https://github.com/leonardt/ast_tools/issues/61
# @m.sequential2(reset_type=m.AsyncReset, pre_passes=[loop_unroll()])
# class EnableShiftRegister:
#     def __init__(self):
#         self.regs = [m.Register(m.UInt[4])() for _ in range(4)]

#     def __call__(self, I: m.UInt[4], shift: m.Bit) -> m.UInt[4]:
#         for i in unroll(range(4)):
#             self.regs[i] = self.regs[i]
#         if shift:
#             self.regs[0] = I
#             for i in unroll(range(3)):
#                 self.regs[i + 1] = self.regs[i].prev()
#         return self.regs[-1].prev()


class EnableShiftRegister(m.Circuit):
    io = m.IO(
        I=m.In(m.UInt[4]),
        shift=m.In(m.Bit),
        O=m.Out(m.UInt[4])
    ) + m.ClockIO(has_async_reset=True)
    regs = [m.Register(m.UInt[4], reset_type=m.AsyncReset, has_enable=True)()
            for _ in range(4)]
    io.O @= m.fold(regs, foldargs={"I": "O"})(io.I, CE=io.shift, CLK=io.CLK,
                                              ASYNCRESET=io.ASYNCRESET)
