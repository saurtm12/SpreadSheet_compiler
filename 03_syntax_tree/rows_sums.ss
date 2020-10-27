function Sum[_rng : range] return scalar is
  scalar sum = 0.0
  for _rng do
    sum := sum + $
  done
  return sum
end

sheet DATA = {
  1.0, 2.0, 3.0, 0.0 ... Last column is for storing the sum of previous values ...
  2.0, 4.0, 8.0, 0.0
  3.0, 6.0, 9.0, 0.0
}

... Variables for later ...
range _starts
range _ends
range _sums
range _sumrange


DATA'D1 := Sum[range DATA'A1..DATA'C1]
DATA'D2 := Sum[range DATA'A2..DATA'C2]
DATA'D3 := Sum[range DATA'A3..DATA'C3]

print_sheet !Direct sums! DATA

... The same with ranges ...

_starts := range DATA'A1..DATA'A3
_ends := range DATA'C1..DATA'C3
_sums := range DATA'D1..DATA'D3

for _starts,_ends do
  _sumrange := range $:_starts..$:_ends
  $:_sums := Sum[ _sumrange ]
done

print_sheet !For sums! DATA
