import numpy as np
n = 8000
x = np.random.normal(0, 1, size=(n, n))
x = x.T.dot(x)
U = np.linalg.cholesky(x)

print(U[5,5])
