import magma as m


class HiLoMultiplier(m.Circuit):
    """
    A 16*16-bit multiplier with separate high and low product outputs
    """
    io = m.IO(A=m.In(m.UInt[16]), B=m.In(m.UInt[16]),
              Hi=m.Out(m.UInt[16]), Lo=m.Out(m.UInt[16]))
    mult = m.zext(io.A, 16) * m.zext(io.B, 16)
    io.Lo @= mult[:16]
    io.Hi @= mult[16:]
