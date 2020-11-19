sheet SS = {
  1.0, 2.0
  3.0, 4.0
}

range _rng = range SS'A1..SS'B1
range _shf = _rng[0,1]

print_sheet !Sheet! SS
print_range !_rng! _rng
print_range !_shf! _shf
