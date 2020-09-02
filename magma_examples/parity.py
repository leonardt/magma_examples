import magma as m


@m.sequential2()
class Parity():
    def __init__(self):
        self.state = m.Register(m.Bit)()

    def __call__(self, I: m.Bit) -> m.Bit:
        if I:
            if self.state == 0:  # was even
                self.state = m.bit(1)  # now odd
            else:  # was odd
                self.state = m.bit(0)  # now even
        return self.state.prev() == 1
