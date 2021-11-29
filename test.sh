# shellcheck disable=SC2129

echo "egl-e1-A.dat" > test.txt
python CARP_solver.py CARP_samples/egl-e1-A.dat -t 600 -s 1 >> test.txt
echo "egl-s1-A.dat" >> test.txt
python CARP_solver.py CARP_samples/egl-s1-A.dat -t 600 -s 1 >> test.txt
echo "gdb1.dat" >> test.txt
python CARP_solver.py CARP_samples/gdb1.dat -t 600 -s 1 >> test.txt
echo "gdb10.dat" >> test.txt
python CARP_solver.py CARP_samples/gdb10.dat -t 600 -s 1 >> test.txt
echo "val1A.dat" >> test.txt
python CARP_solver.py CARP_samples/val1A.dat -t 600 -s 1 >> test.txt
echo "val4A.dat" >> test.txt
python CARP_solver.py CARP_samples/val4A.dat -t 600 -s 1 >> test.txt
echo "val7A.dat" >> test.txt
python CARP_solver.py CARP_samples/val7A.dat -t 600 -s 1 >> test.txt
