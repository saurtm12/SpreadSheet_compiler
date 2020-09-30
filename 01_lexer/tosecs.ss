... hours, minutus to seconds ...

function To_seconds[ hours : scalar, minutes : scalar] return scalar is
  scalar retval
  retval := (hours*60.0*60.0) + (minutes*60.0)
  return retval
end 

print_scalar !1 hour 3 minutes (3780)! To_seconds[1.0,3.0]
print_scalar !2 hours (7200)! To_seconds[ 2.0, 0.0 ]
print_scalar !zero (0)! To_seconds[0.0, 0.0 ]
