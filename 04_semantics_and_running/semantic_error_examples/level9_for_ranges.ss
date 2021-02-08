sheet SS = 5 * 5

range _rng1 = range SS'A1..SS'A5
range _rng2 = _rng1[1,0]
range _rng3 = _rng1[2,0]

... These should be ok ...
for _rng1,_rng2
do
  $:_rng1 := $:_rng2
done

for _rng1
do
  for _rng2
  do
    $:_rng2 := 2.0
  done
done

... This should work, if you allow selecting ranges from nested for loops ...
for _rng1
do
  for _rng2
  do
    $:_rng1 := 3.0
    $:_rng2 := 2.0
  done
done

... This should fail ...
for _rng1,_rng2
do
  $:_rng1 := $:_rng3
done

print_scalar 0.0
