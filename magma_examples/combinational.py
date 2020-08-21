import magma as m


@m.combinational2()
def add(x: m.UInt[16], y: m.UInt[16]) -> m.UInt[16]:
    return x + y
