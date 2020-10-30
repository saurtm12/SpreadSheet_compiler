... Create a sheet and add a sliding average ...

sheet INDATA = { 1.0 4.0 9.0 16.0 25.0 36.0 49.0 64.0 81.0 100.0 } ... Heehee, nice way to create a row vector in our syntax! ...
sheet OUTDATA = 2 * 10

function Average[_rng : range] return scalar is
  scalar avgtmp = 0.0
  for _rng do
    avgtmp := avgtmp + $
  done
  print_scalar avgtmp / #_rng
  return avgtmp / #_rng ... # gives the size of a range ...
end

range _windowstart = range OUTDATA'A1..OUTDATA'A8 ... Range defining where averaging window starts ...
range _windowend = _windowstart[0,2] ... Window ends 2 rows below the start ...
range _avgresult = _windowstart[1,1]  ... Calculate results to the right of the middle of input data ...
range _window

OUTDATA := INDATA
print_sheet OUTDATA

for _windowstart,_windowend,_avgresult do
  _window := range $:_windowstart .. $:_windowend ... Averaging window is from start to end ...
  $:_avgresult := Average[_window]
done

print_sheet OUTDATA
