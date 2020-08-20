import magma as m
from .full_adder import FullAdder


# A 4-bit adder with carry in and carry out
class Adder4(m.Circuit):
    io = m.IO(
        A=m.In(m.UInt[4]),
        B=m.In(m.UInt[4]),
        CIN=m.In(m.Bit),
        SUM=m.Out(m.UInt[4]),
        COUT=m.Out(m.Bit)
    )
    curr_cin = io.CIN
    for i in range(4):
        next_sum, curr_cin = FullAdder()(io.A[i], io.B[i], curr_cin)
        io.SUM[i] @= next_sum
    io.COUT @= curr_cin
