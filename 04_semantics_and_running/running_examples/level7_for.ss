sheet SS = 5 * 2

range _row1 = range SS'A1..SS'E1
range _row2 = _row1[0,1] ... Range one row down ...

scalar nn = 1.0

print_sheet !SS originally: ! SS

for _row1
do
  $ := nn
  nn := nn + 1.0
  print_scalar !In for, nn = ! nn
done

print_sheet !SS after first for: ! SS

... Range expression directly in for ...
for range SS'B1..SS'C1
do
  print_scalar !Cell: ! $
done
