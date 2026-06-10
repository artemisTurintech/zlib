/* benchmark.c -- throughput benchmark for zlib compress/decompress */

#if defined(_WIN32) && !defined(_CRT_SECURE_NO_WARNINGS)
#  define _CRT_SECURE_NO_WARNINGS
#endif

#include "zlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
#  include <windows.h>
static double now_sec(void) {
    LARGE_INTEGER t, f;
    QueryPerformanceCounter(&t);
    QueryPerformanceFrequency(&f);
    return (double)t.QuadPart / (double)f.QuadPart;
}
#else
static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}
#endif

#define BUF_SIZE (4 * 1024 * 1024)  /* 4 MB input */
#define ITERATIONS 20

static void fill_buffer(unsigned char *buf, size_t len) {
    /* mix of runs and pseudo-random bytes for a realistic ratio */
    size_t i = 0;
    while (i < len) {
        size_t run = 8 + (i % 64);
        unsigned char c = (unsigned char)(i * 17 + 33);
        if (i + run > len) run = len - i;
        memset(buf + i, c, run);
        i += run;
    }
}

int main(void) {
    unsigned char *src = (unsigned char *)malloc(BUF_SIZE);
    uLong bound = compressBound(BUF_SIZE);
    unsigned char *comp = (unsigned char *)malloc(bound);
    unsigned char *decomp = (unsigned char *)malloc(BUF_SIZE);
    if (!src || !comp || !decomp) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    fill_buffer(src, BUF_SIZE);

    /* --- compress benchmark --- */
    uLong comp_len = bound;
    if (compress2(comp, &comp_len, src, BUF_SIZE, Z_DEFAULT_COMPRESSION) != Z_OK) {
        fprintf(stderr, "compress2 failed\n");
        return 1;
    }
    double ratio = (double)comp_len / BUF_SIZE * 100.0;

    double t0 = now_sec();
    for (int i = 0; i < ITERATIONS; i++) {
        uLong cl = bound;
        compress2(comp, &cl, src, BUF_SIZE, Z_DEFAULT_COMPRESSION);
    }
    double elapsed_c = now_sec() - t0;
    double mb_c = (double)BUF_SIZE * ITERATIONS / (1024.0 * 1024.0);

    /* --- decompress benchmark --- */
    t0 = now_sec();
    for (int i = 0; i < ITERATIONS; i++) {
        uLong dl = BUF_SIZE;
        uncompress(decomp, &dl, comp, comp_len);
    }
    double elapsed_d = now_sec() - t0;
    double mb_d = (double)BUF_SIZE * ITERATIONS / (1024.0 * 1024.0);

    if (memcmp(src, decomp, BUF_SIZE) != 0) {
        fprintf(stderr, "decompress round-trip mismatch!\n");
        return 1;
    }

    printf("zlib benchmark (%d MB input x %d iterations)\n",
           BUF_SIZE / (1024 * 1024), ITERATIONS);
    printf("  compress ratio : %.1f%%\n", ratio);
    printf("  compress       : %.1f MB/s\n", mb_c / elapsed_c);
    printf("  decompress     : %.1f MB/s\n", mb_d / elapsed_d);

    free(src); free(comp); free(decomp);
    return 0;
}
