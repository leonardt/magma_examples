import fault

from magma_examples.life import Life


def test_life(capsys):
    Life10 = Life(10, 10)
    tester = fault.SynchronousTester(Life10, Life10.CLK)

    def set_mode(run: bool):
        tester.circuit.running = run
        tester.advance_cycle()

    def clear_board():
        tester.circuit.write_value = 0
        for i in range(10):
            for j in range(10):
                tester.circuit.write_row_address = i
                tester.circuit.write_col_address = j
                tester.advance_cycle()

    def init_glider():
        clear_board()
        tester.circuit.write_value = 1
        tester.circuit.write_row_address = 3
        for addr in (3, 5):
            tester.circuit.write_col_address = addr
            tester.advance_cycle()

        tester.circuit.write_row_address = 4
        for addr in (4, 5):
            tester.circuit.write_col_address = addr
            tester.advance_cycle()

        tester.circuit.write_row_address = 5
        tester.circuit.write_col_address = 4
        tester.advance_cycle()

    def print_board():
        tester.print("   ")
        for i in range(10):
            tester.print(" " + str(i)[-1])
        tester.print("\n")

        for i in range(10):
            tester.print(f"{i:2d} ")
            for j in range(10):
                if_tester = tester._if(tester.circuit.state[(j, i)])
                if_tester.print(" *")
                if_tester._else().print("  ")
            tester.print("\n")
        tester.print("\n")

    set_mode(run=False)
    init_glider()
    print_board()
    set_mode(run=True)
    for time in range(20):
        tester.print(f"Period: {time}\n")
        print_board()
        tester.advance_cycle()


    tester.compile_and_run("verilator", disp_type="realtime")

    out, _ = capsys.readouterr()
    expected = """\
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3        *   *
 4          * *
 5          *
 6
 7
 8
 9

Period: 0
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3            *
 4        *   *
 5          * *
 6
 7
 8
 9

Period: 1
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3          *
 4            * *
 5          * *
 6
 7
 8
 9

Period: 2
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3            *
 4              *
 5          * * *
 6
 7
 8
 9

Period: 3
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4          *   *
 5            * *
 6            *
 7
 8
 9

Period: 4
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4              *
 5          *   *
 6            * *
 7
 8
 9

Period: 5
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4            *
 5              * *
 6            * *
 7
 8
 9

Period: 6
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4              *
 5                *
 6            * * *
 7
 8
 9

Period: 7
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5            *   *
 6              * *
 7              *
 8
 9

Period: 8
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5                *
 6            *   *
 7              * *
 8
 9

Period: 9
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5              *
 6                * *
 7              * *
 8
 9

Period: 10
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5                *
 6                  *
 7              * * *
 8
 9

Period: 11
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6              *   *
 7                * *
 8                *
 9

Period: 12
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6                  *
 7              *   *
 8                * *
 9

Period: 13
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6                *
 7                  * *
 8                * *
 9

Period: 14
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6                  *
 7                    *
 8                * * *
 9

Period: 15
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6
 7                *   *
 8                  * *
 9                  *

Period: 16
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6
 7                    *
 8                *   *
 9                  * *

Period: 17
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6
 7                  *
 8  *                 *
 9                  * *

Period: 18
    0 1 2 3 4 5 6 7 8 9
 0
 1
 2
 3
 4
 5
 6
 7                    *
 8  *
 9  *               * *

Period: 19
    0 1 2 3 4 5 6 7 8 9
 0                    *
 1
 2
 3
 4
 5
 6
 7
 8  *               *
 9  *                 *

""".splitlines()
    # Ignore </STDOUT> separater (last line)
    assert out.splitlines()[-len(expected) - 1:-1] == expected
