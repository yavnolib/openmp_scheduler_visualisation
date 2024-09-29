#include <stdio.h>
#include <omp.h>
#include <math.h>

double some_difficult_func(int i) {
    return sin(1e5 / i);
}

void log_thread_iter(int i, int thread_num) {
    // iter<->thread_num
    printf("%d<->%d\n", i, thread_num);
}


int main(int argc, char* argv[]) {
    int i;
    double sin_res = 0.;

    if (argc != 3) {
        printf("Use: %s <num_iterations> <num_threads>\n", argv[0]);
        return 1;
    }
    
    char *endptr1, *endptr2;
    int num_iterations = strtol(argv[1], &endptr1, 10);
    if (*endptr1 != '\0' || num_iterations <= 0) {
        num_iterations = 65;
        printf("num_iterations is set to default: %d\n", num_iterations);
    }
    int num_threads = strtol(argv[2], &endptr2, 10);
    if (*endptr1 != '\0' || num_threads <= 0) {
        num_threads = 4;
        printf("num_threads is set to default: %d\n", num_threads);
    }



    omp_set_num_threads(num_threads);
    freopen("logs.txt", "w", stdout);

    // ------------ Schedule default ------------------------
    printf("Default schedule:\n:::");
    #pragma omp parallel for
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }


    // ------------ Schedule static ------------------------
    printf("\n:::Static schedule, chunk=1:\n:::");
    #pragma omp parallel for schedule(static, 1)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    printf("\n:::Static schedule, chunk=4:\n:::");
    #pragma omp parallel for schedule(static, 4)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    // --------------- Schedule dynamic ---------------------
    printf("\n:::Dynamic schedule, chunk=1:\n:::");
    #pragma omp parallel for schedule(dynamic, 1)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    printf("\n:::Dynamic schedule, chunk=4:\n:::");
    #pragma omp parallel for schedule(dynamic, 4)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    // --------------- Schedule guided -----------------------
    printf("\n:::Guided schedule, chunk=1:\n:::");
    #pragma omp parallel for schedule(guided, 1)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    printf("\n:::Guided schedule, chunk=4:\n:::");
    #pragma omp parallel for schedule(guided, 4)
    for (i = 0; i < num_iterations; i++) {
        sin_res = some_difficult_func(i);
        log_thread_iter(i, omp_get_thread_num());
    }

    return 0;
}
