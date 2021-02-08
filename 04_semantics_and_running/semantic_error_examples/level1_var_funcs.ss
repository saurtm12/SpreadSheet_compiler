scalar ss = 3.0

subroutine Fu[] is
  print_scalar !In Func! 0.0
end

... These should fail ...
scalar ss = 4.0

function Fu[] return scalar is
  return 0.0
end

... These should work (after removing double definitions) ...
Fu[]
print_scalar ss

... These should give an error (remove the other line to test just one of these) ...
print_scalar tt ... Undefined variable ...
Gu[] ... Undefined subroutine ...
