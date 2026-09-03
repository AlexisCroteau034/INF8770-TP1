/* =============================================================================
 * Module d'Algebre Lineaire et Manipulation Memoire en C (C99)
 * ============================================================================= */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>

#define MATRIX_MAX_DIM 32
#define STATUS_OK 0
#define STATUS_ERROR -1

typedef struct {
    size_t rows;
    size_t cols;
    double data[MATRIX_MAX_DIM][MATRIX_MAX_DIM];
} Matrix;

Matrix matrix_zero(size_t rows, size_t cols) {
    Matrix m;
    m.rows = (rows <= MATRIX_MAX_DIM) ? rows : MATRIX_MAX_DIM;
    m.cols = (cols <= MATRIX_MAX_DIM) ? cols : MATRIX_MAX_DIM;
    for (size_t i = 0; i < m.rows; ++i) {
        for (size_t j = 0; j < m.cols; ++j) {
            m.data[i][j] = 0.0;
        }
    }
    return m;
}

Matrix matrix_identity(size_t dim) {
    Matrix m = matrix_zero(dim, dim);
    for (size_t i = 0; i < m.rows; ++i) {
        m.data[i][i] = 1.0;
    }
    return m;
}

int matrix_add(const Matrix *a, const Matrix *b, Matrix *out) {
    if (!a || !b || !out || a->rows != b->rows || a->cols != b->cols) {
        return STATUS_ERROR;
    }
    out->rows = a->rows;
    out->cols = b->cols;
    for (size_t i = 0; i < a->rows; ++i) {
        for (size_t j = 0; j < b->cols; ++j) {
            out->data[i][j] = a->data[i][j] + b->data[i][j];
        }
    }
    return STATUS_OK;
}

int matrix_multiply(const Matrix *a, const Matrix *b, Matrix *out) {
    if (!a || !b || !out || a->cols != b->rows) {
        return STATUS_ERROR;
    }
    out->rows = a->rows;
    out->cols = b->cols;
    for (size_t i = 0; i < a->rows; ++i) {
        for (size_t j = 0; j < b->cols; ++j) {
            double sum = 0.0;
            for (size_t k = 0; k < a->cols; ++k) {
                sum += a->elements[i][k] * b->elements[k][j];
            }
            out->data[i][j] = sum;
        }
    }
    return STATUS_OK;
}

double vector_euclidean_norm(const double *vec, size_t length) {
    if (!vec || length == 0) return 0.0;
    double sum_sq = 0.0;
    for (size_t i = 0; i < length; ++i) {
        sum_sq += vec[i] * vec[i];
    }
    return sqrt(sum_sq);
}
