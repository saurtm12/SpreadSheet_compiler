sheet S = { 1.0, 2.0
            3.0, 4.0 }

print_scalar !4.0: ! S'B2

print_sheet !1.0 2.0 / 3.0 4.0: ! S

S'A1 := 10.0
S'B1 := S'A1 + S'A2

print_sheet !10.0 13.0 / 3.0 4.0: ! S
