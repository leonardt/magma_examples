import magma as m


class BasicALU(m.Circuit):
    io = m.IO(a=m.In(m.UInt[4]), b=m.In(m.UInt[4]), opcode=m.In(m.UInt[4]),
              out=m.Out(m.UInt[4]))

    @m.inline_combinational()
    def logic():
        if io.opcode == 0:
            io.out @= io.a
        elif io.opcode == 1:
            io.out @= io.b
        elif io.opcode == 2:
            io.out @= io.a + 1
        elif io.opcode == 3:
            io.out @= io.a - 1
        elif io.opcode == 4:
            io.out @= io.a + 4
        elif io.opcode == 5:
            io.out @= io.a - 4
        elif io.opcode == 6:
            io.out @= io.a + io.b
        elif io.opcode == 7:
            io.out @= io.a - io.b
        elif io.opcode == 8:
            io.out @= m.uint(io.a < io.b, 4)
        else:
            io.out @= m.uint(io.a == io.b, 4)


class SimpleALU(m.Circuit):
    io = m.IO(a=m.In(m.UInt[4]), b=m.In(m.UInt[4]), opcode=m.In(m.UInt[2]),
              out=m.Out(m.UInt[4]))

    @m.inline_combinational()
    def logic():
        if io.opcode == 0:
            io.out @= io.a + io.b
        elif io.opcode == 1:
            io.out @= io.a - io.b
        elif io.opcode == 2:
            io.out @= io.a
        else:
            io.out @= io.b
