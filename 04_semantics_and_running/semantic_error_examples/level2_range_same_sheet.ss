sheet S = { 1.0 }
sheet T = { 2.0 }

... This should work ...
print_range range S'A1..S'A1

... This shouldn't work ...
print_range range S'A1..T'A1
