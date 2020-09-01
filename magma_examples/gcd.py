import magma as m


@m.sequential2()
class GCD:
    def __init__(self):
        self.x = m.Register(m.UInt[16])()
        self.y = m.Register(m.UInt[16])()

    def __call__(self, a: m.In(m.UInt[16]), b: m.In(m.UInt[16]),
                 load: m.In(m.Bit)) -> (m.Out(m.UInt[16]), m.Out(m.Bit)):
        if load:
            self.x = a
            self.y = b
        elif self.y != 0:
            if self.x > self.y:
                self.x = self.x - self.y
            else:
                self.y = self.y - self.x
        return self.x.prev(), self.y.prev() == 0
