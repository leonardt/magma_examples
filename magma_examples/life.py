from functools import reduce
import magma as m


class Cell(m.Circuit):
    io = m.IO(
        neighbors=m.In(m.Bits[8]),
        out=m.Out(m.Bit),
        running=m.In(m.Bit),
        write_enable=m.In(m.Bit),
        write_value=m.In(m.Bit)
    ) + m.ClockIO()
    is_alive = m.Register(m.Bit)()

    count = reduce(lambda x, y: x + m.uint(y, 3), io.neighbors, 
                   m.uint(0, 3))

    @m.inline_combinational()
    def logic():
        if ~io.running:
            if io.write_enable:
                is_alive.I @= io.write_value
            else:
                is_alive.I @= is_alive.O
        else:
            if is_alive.O:
                if count < 2:
                    is_alive.I @= False
                elif count < 4:
                    is_alive.I @= True
                else:
                    is_alive.I @= False
            else:
                if ~is_alive.O & (count == 3):
                    is_alive.I @= True
                else:
                    is_alive.I @= False

        io.out @= is_alive.O


class Life(m.Generator2):
    def __init__(self, rows: int, cols: int):
        self.io = io = m.IO(
            state=m.Out(m.Array[(cols, rows), m.Bit]),
            running=m.In(m.Bit),
            write_value=m.In(m.Bit),
            write_row_address=m.In(m.UInt[m.bitutils.clog2(rows + 1)]),
            write_col_address=m.In(m.UInt[m.bitutils.clog2(cols + 1)])
        ) + m.ClockIO()

        cells = [[Cell(name=f"cell_{i}x{j}") for i in range(cols)] 
                 for j in range(rows)]
        for row in range(rows):
            for col in range(cols):
                cell = cells[row][col]
                io.state[col, row] @= cell.out
                cell.running @= io.running
                cell.write_value @= io.write_value
                cell.write_enable @= ((io.write_row_address == row) & 
                                      (io.write_col_address == col))

        def get_neighbor_index(row, row_delta, col, col_delta):
            def wrap_index(index, delta, max_):
                if index == 0 and delta == -1:
                    return max_ - 1
                elif index == max_ - 1 and delta == 1:
                    return 0
                return index + delta
            return (wrap_index(row, row_delta, rows), 
                    wrap_index(col, col_delta, cols))

        for row in range(rows):
            for col in range(cols):
                cell = cells[row][col]
                neighbor_input = 0
                for delta_row in range(-1, 2):
                    for delta_col in range(-1, 2):
                        if delta_row == 0 and delta_col == 0:
                            continue
                        row_index, col_index = get_neighbor_index(
                            row, delta_row, col, delta_col)
                        cell.neighbors[neighbor_input] @= \
                            cells[row_index][col_index].out
                        neighbor_input += 1
