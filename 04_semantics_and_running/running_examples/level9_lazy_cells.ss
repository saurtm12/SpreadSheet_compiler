sheet A = 1*5
sheet B = 1*1
scalar aa
scalar value
range _bar

... Returns the second parameter if first parameter condition is true, otherwise returns the third parameter ...
function If[cond:scalar, true:scalar, false:scalar] return scalar
is
  if cond
  then
    return true
  else
    return false
  endif
end

... The value of this cell determines what cells in A will be 1, which 0 ...
B'A1 := 0.0

_bar := range A'A1..A'A5
value := 5.0
for _bar
do
  $ := If[ B'A1 >= value, 1.0, 0.0 ] ... assign lazy expression to the cell, depends on value of B'A1 ...
  value := value + 5.0
done

... Should print out an increasing number of 1s, row by row ...
aa := 0.0
while aa < 30.0 
do
  B'A0 := aa
  print_sheet !Bar diagram! A
  aa := aa + 5.0
done
