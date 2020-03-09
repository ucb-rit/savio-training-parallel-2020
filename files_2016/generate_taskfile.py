m = 50
n = 1000
file = open("taskfile", "w")
for i in range(1,(m+1)):
    file.write("sh -c \"module load python/2.7.8 numpy; ./compute.py -i " + str(i) + " -n " + str(n) + " -p exp_output1\"\n")
n = 2000
for i in range(1,(m+1)):
    file.write("sh -c \"module load python/2.7.8 numpy; ./compute.py -i " + str(i) + " -n " + str(n) + " -p exp_output2\"\n")

