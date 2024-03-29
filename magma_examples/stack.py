import magma as m


class Stack(m.Generator2):
    def __init__(self, depth):
        self.io = io = m.IO(
            push=m.In(m.Bit),
            pop=m.In(m.Bit),
            en=m.In(m.Bit),
            data_in=m.In(m.UInt[32]),
            data_out=m.Out(m.UInt[32]),
        ) + m.ClockIO()

        stack_mem = m.Memory(depth, m.UInt[32])()
        stack_pointer = m.Register(m.UInt[m.bitutils.clog2(depth + 1)])()
        out_reg = m.Register(m.UInt[32])()

        wen = io.en & io.push & (stack_pointer.O < depth)
        stack_mem.WE @= m.enable(wen)
        stack_mem.WDATA @= io.data_in
        stack_mem.WADDR @= stack_pointer.O[:-1]

        stack_mem.RADDR @= stack_pointer.O[:-1] - 1

        with m.when(wen):
            stack_pointer.I @= stack_pointer.O + 1
        with m.elsewhen(io.en & io.pop & (stack_pointer.O > 0)):
            stack_pointer.I @= stack_pointer.O - 1

        with m.when(stack_pointer.O > 0):
            out_reg.I @= stack_mem.RDATA
        io.data_out @= out_reg.O
