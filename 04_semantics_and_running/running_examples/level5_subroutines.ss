subroutine Sub[] is
  scalar local = 42.0
  print_scalar !Sub: ! local
end

subroutine Subpar[par:scalar] is
  print_scalar !Subpar parameter: ! par
end

scalar two = 2.0

print_scalar !Start: ! 0.0
Sub[]
Subpar[1.0]
Subpar[1.0 + two]
print_scalar !End: ! 0.0
