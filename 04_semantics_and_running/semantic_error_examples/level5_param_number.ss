function Fun[aa:scalar, bb:scalar] return scalar is
  return 0.0
end

subroutine Sub[cc:scalar] is
  print_scalar 0.0
end

... These should be ok ...
Sub[3.0]
print_scalar Fun[1.0, 2.0]

... These should produce an error ...
Sub[]
print_scalar Fun[1.0, 2.0, 3.0]
