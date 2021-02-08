scalar nn = 1.0
scalar fact = 1.0

scalar stop = 10.0

while nn <= stop do
  fact := nn * fact
  print_scalar !nn = ! nn
  print_scalar !nn's factorial = ! fact
  if fact > 1000.0 then
    print_scalar !Wow, large number: ! fact
  endif
  if fact > 100000.0 then
    print_scalar !Wow, HUGE number: ! fact
  else
    print_scalar !Still not HUGE: ! fact
  endif
  nn := nn + 1.0
done

