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

... Multi-range for ...
for _row1,_row2
do
  $:_row2 := $:_row1 * 2.0
done

print_sheet !SS after second for: ! SS
