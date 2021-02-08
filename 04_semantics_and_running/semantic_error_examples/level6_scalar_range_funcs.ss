sheet S = { 1.0 }

function Funsclr[] return scalar is
  return 0.0
end

function Funrng[] return range is
  return range S'A1..S'A1
end

... These should be ok ...
print_scalar Funsclr[]
print_range [ Funrng[] ]

... These should produce an error ...
print_scalar Funrng[]
print_range [ Funsclr[] ]
