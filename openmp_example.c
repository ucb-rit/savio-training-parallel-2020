#include <stdio.h>
#include <omp.h> // needed when using any openMP functions like omp_get_thread_num()

// comipile with:  gcc -fopenmp openmp_example.c -o openmp-example



void myFun(double *in, int id)
{
  // this is just the scaffolding for a function
}

int main()
{
  int nThreads, myID;
  double* input;
  /* make the values of nThreads and myid private to each thread */
#pragma omp parallel private (nThreads, myID)
  { // beginning of block
    myID = omp_get_thread_num();
    printf("Hello I am thread %i\n", myID);
    myFun(input, myID);  // do some computation on each thread
    /* only master node print the number of threads */
    if (myID == 0)
      {
	nThreads = omp_get_num_threads();
	printf("I'm the boss and control %i threads. How come they're in front of me?\n", nThreads);
      }
  } // end of block
  return 0;
} 
