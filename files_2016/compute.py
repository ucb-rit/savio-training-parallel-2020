#!/usr/bin/env python

def calculate(i, n, m, sd):
    np.random.seed(i)  # careful, this doesn't guarantee truly independent draws across the various calls to calculate() with different 'i' values
    mat = np.random.normal(m, sd, size = (n,n))
    C = mat.T.dot(mat)
    vals = np.linalg.eigvalsh(C) 
    out1 = sum(np.log(vals))
    out2 = vals[n-1]/vals[0]
    return(out1, out2)

if __name__ == '__main__':
    import argparse
    import numpy as np
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', help = "ID of run")
    parser.add_argument('-n', '--size', default=1000, help = "matrix dimension")
    parser.add_argument('-m', '--mean', default=0,
        help='mean of matrix elements')
    parser.add_argument('-s', '--sd', default=1,
        help='standard deviation of matrix elements')
    parser.add_argument('-p', '--path', default='.',
        help='path to write output files to')
    args = parser.parse_args()
    out = calculate(int(args.id), int(args.size), float(args.mean), float(args.sd))
    file = open(args.path + "/output" + args.id + ".txt", "w")
    file.write("%s,%s\n" % (out))
