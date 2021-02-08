scalar one = 1.0
scalar two = 2.0

scalar five = two + 3.0

print_scalar one
print_scalar !Should be 3.0: ! one + two
print_scalar !Should be 6.0: ! one + five
print_scalar !Should be 24.0: ! two * 3.0 * 4.0
print_scalar !Should be 0.0: ! 3.0 - 2.0 - one
print_scalar !Should be 50.0: ! 10.0 + 20.0 * (4.0 - two)

two := 4.0
print_scalar !Should be 5.0: ! one + two
