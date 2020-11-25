function Fun[] return scalar is
  return 0.0
end

subroutine Sub[] is
  print_scalar 0.0
end

... These should be ok ...
Sub[]
print_scalar Fun[]

... These should produce an error ...
Fun[]
print_scalar Sub[]
