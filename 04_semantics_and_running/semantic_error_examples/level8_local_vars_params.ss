scalar global = 0.0

... These should be ok ...
function Fun[aa:scalar, bb:scalar] return scalar is
  return aa + bb + global
end

subroutine Sub[cc:scalar] is
  scalar dd = 2.0
  print_scalar cc + dd
end

... These should be fail ...
subroutine Sub_fail[] is
  print_scalar aa + dd
end

print_scalar cc
