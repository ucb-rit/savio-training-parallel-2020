
#include <stdio.h>
#include<mpi.h>
#include <utmpx.h>

int main( int argc , char **argv )
{
MPI_Init(&argc, &argv);

int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Print off a hello world message
printf("Hello %s from processor %s, rank %d out of %d processors\n",
                    argv[1], processor_name, world_rank, world_size);

//printf( "cpu = %d\n", sched_getcpu() );
MPI_Finalize();
return 0;
