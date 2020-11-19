function Sum[ _aa : range ] return scalar is
  scalar sum
  sum := 0.0
  for _aa do
    sum := sum + $
  done
  return sum
end

function Average[ _aa : range ] return scalar is
  if #_aa = 0.0
  then
    return 0.0
  else
    return Sum[ _aa ] / #_aa
  endif
end

subroutine Map_lazy_incr[ _in : range , _out : range ] is
  for _in,_out do
    $:_out := $:_in + 1.0
  done
end

subroutine Map_eager_incr[ _in : range , _out : range ] is
  scalar ss
  for _in,_out do
    ss := $:_in + 1.0
    $:_out := ss
  done
end

function Max[ _aa : range ] return scalar is
  scalar max
  max := 0.0
  for _aa do
    if( $ > max ) then max := $ endif 
  done
  return max
end
