import magma as m
from mantle import RegFileBuilder


class Risc(m.Circuit):
    io = m.IO(
        is_write=m.In(m.Bit),
        write_addr=m.In(m.UInt[8]),
        write_data=m.In(m.UInt[32]),
        boot=m.In(m.Bit),
        valid=m.Out(m.Bit),
        out=m.Out(m.UInt[32])
    ) + m.ClockIO(has_async_reset=True)
    file = RegFileBuilder("file", 256, 32, write_forward=False)
    code = RegFileBuilder("code", 256, 32, write_forward=False)
    pc = m.Register(m.UInt[8])()

    instr = code[pc.O]

    op = instr[24:]
    rci = instr[16:24]
    rai = instr[8:16]
    rbi = instr[:8]

    ra = m.mux([file[rai], 0], rai == 0)
    rb = m.mux([file[rbi], 0], rbi == 0)
    rc = m.Bits[32]()
    io.out @= rc

    code.write(io.write_addr, io.write_data, enable=io.is_write)
    file.write(rci, rc, enable=(rci != 255))

    @m.inline_combinational()
    def logic():
        rc @= m.Bits[32](0)
        io.valid @= False
        if io.is_write:
            pc.I @= pc.O
        elif io.boot:
            pc.I @= 0
        else:
            if op == 0:
                rc @= ra + rb
            elif op == 1:
                rc @= m.zext((rai << 8) | rbi, 24)
            if rci == 255:
                io.valid @= True
            pc.I @= pc.O + 1
