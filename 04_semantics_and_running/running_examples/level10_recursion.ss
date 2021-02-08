function Factorial[nn : scalar] return scalar is
  scalar fact = nn
  scalar factprev = 1.0
  print_scalar !In func, nn = ! nn
  if nn > 1.0 then
     factprev := Factorial[nn - 1.0]
  endif
  fact := fact * factprev
  return fact
end

print_scalar !Factorial of 6 is 720: ! Factorial[6.0]
