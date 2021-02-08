sheet S = { 1.0 }

... These should compile ...
function Funsclr_ok[] return scalar is
  return 0.0
end

function Funrng_ok[] return range is
  return range S'A1..S'A1
end

... These should not ...
subroutine Sub_fail[] is
  return 0.0
end

function Funsclr_fail[] return scalar is
  return range S'A1..S'A1
end

function Funrng_fail[] return range is
  return 0.0
end

... Compulsory statement ...
print_scalar 0.0
