function Fun[] return scalar is
  scalar local = 42.0
  return local
end

function Funpar[par:scalar] return scalar is
  return 2.0 * par
end

scalar two = 2.0

print_scalar !Start: ! 0.0
print_scalar !Fun[]: ! Fun[]
print_scalar !Funpar[1.0]: ! Funpar[1.0]
print_scalar !Funpar[3.0]: ! Funpar[1.0 + two]
print_scalar !End: ! 0.0
