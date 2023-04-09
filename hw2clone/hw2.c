/* It computes matrix multiplication. Reads two matrix, multiply them, stores the result matrix */
/* Usage: ./hw2 data1.bin data2.bin res.bin N */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <sys/wait.h>

#include "wrapper.h"
#include "timeft.h"

// 파일의 크기를 이용해 배열의 크기를 구하는 함수
int GetMatrixSize(int fd) {
    int size;
    struct stat st;

    if (fstat(fd, &st) < 0) {
        perror("matrix size err");
        exit(1);
    }
    size = st.st_size;
    return (int)sqrt(size / sizeof(double));

}

// childSize개의 프로세스에게 NxN행렬을 분배하는 함수, 방법 1사용
int* DivideRowsByChild(int childSize, int N) {
    int* sizeList = (int*)malloc(sizeof(int) * childSize);

    if (N % childSize == 0) {
        for (int i = 0; i < childSize; i++) {
            sizeList[i] = N / childSize;
        }

        return sizeList;
    }

    int r = N % childSize;

    for (int i = 0; i < r; i++) {
        sizeList[i] = (N / childSize) + 1;
    }

    for (int i = r; i < childSize; i++) {
        sizeList[i] = (N / childSize);
    }


    return sizeList;

}

// 배열의 누적합을 구해 각 프로세스가 접근하기 시작하는 행의 시작 index를 구하는 함수
int* CalculateStartIndex(int* arr, int size) {
    int* result = (int*)malloc(sizeof(int) * size);

    result[0] = 0;


    for (int i = 1; i < size; i++) {
        int sum = 0;

        for (int j = 0; j < i; j++) {
            sum += arr[j];
        }

        result[i] = sum;
    }

    return result;

}


int main(int argc, char* argv[])
{
    // 에러 처리
    if (argc != 5) {
        perror("Usage: ./hw2 infile1 infile2 outfile <p>");
        exit(1);
    }

    int ifd1, ifd2, ofd;
    int N, N2, childSize;
    struct stat st_file1;
    pid_t pid;


    // 파일의 값을 읽어올 두 행렬과 결과 행렬
    double** arr1 = NULL;
    double** arr2 = NULL;
    double** res = NULL;

    ifd1 = Open(argv[1], O_RDONLY);
    ifd2 = Open(argv[2], O_RDONLY);
    ofd = Creat(argv[3], 0644);

    close(ofd);

    N = GetMatrixSize(ifd1);
    N2 = GetMatrixSize(ifd2);

    fstat(ifd1, &st_file1);


    // 에러 처리
    childSize = atoi(argv[4]);
    if (childSize < 1) {
        perror("Error: The 4th parameter should be an integer greater than zero");
        exit(1);
    }


    if (st_file1.st_size != N * N * sizeof(double)) {
        perror("Error: The 1st input file size is not n*n");
        exit(1);
    }

    if (N != N2) {
        perror("Error: The 2nd input file size is not the same as the 1st one");
        exit(1);
    }

    // 2차원 행렬 메모리 할당
    arr1 = (double**)malloc(sizeof(double*) * N);
    arr2 = (double**)malloc(sizeof(double*) * N);



    for (int i = 0; i < N; i++) {
        arr1[i] = (double*)malloc(sizeof(double) * N);
        arr2[i] = (double*)malloc(sizeof(double) * N);
    }

    // arg 1번,2번 파일의 행렬에 읽어 arr1, 2번에 저장
    // arg 1번 파일의 행렬 읽어 arr1에 저장
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            Read(ifd1, &arr1[i][j], sizeof(double));
        }
    }

    // arg 2번 파일의 행렬 읽어 arr2에 저장
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            Read(ifd2, &arr2[i][j], sizeof(double));
        }
    }


    // dividedRow는 자식 프로세스가 할당받은 행의 갯수를 의미
    // startIndexes는 각 자식 프로세스가 시작해야하는 행을 의미한다.
    // 즉 0번쨰 프로세스라면 startIndexes[0]에서 부터 dividedRow[0]개만큼 수행해야함을 의미 
    int* dividedRow = DivideRowsByChild(childSize, N);
    int* startIndexes = CalculateStartIndex(dividedRow, childSize);


    init_timelog(childSize);
    for (int i = 0; i < childSize; i++) {
        pid = fork();

        // fork() 함수 호출 실패
        if (pid < 0) {
            perror("fork Error");
            exit(1);
        }
        // 자식 프로세스
        else if (pid == 0) {


            int startIdx = startIndexes[i];
            int endIdx = startIdx + dividedRow[i];
            int resultSize = endIdx - startIdx;
            int ofdChild;
            struct flock file_lock;

            ofdChild = open(argv[3], O_RDWR);

            // 행렬곱을 저장할 결과 배열 메모리 할당
            res = (double**)malloc(sizeof(double*) * resultSize);
            for (int i = 0; i < resultSize; i++) {
                res[i] = (double*)malloc(sizeof(double) * N);
            }

            // 행렬곱 측정
            start_timelog(i);
            for (int row = 0; row < resultSize; row++) {
                for (int col = 0; col < N; col++) {
                    res[row][col] = 0.0;
                    for (int k = 0; k < N; k++) {
                        res[row][col] += arr1[row + startIdx][k] * arr2[k][col]; // 행렬 곱 계산   
                    }
                }
            }
            finish_timelog(i);



            // 파일 커서 이동후 파일에 값 저장
            for (int row = 0; row < resultSize; row++) {
                for (int col = 0; col < N; col++) {


                    file_lock.l_type = F_WRLCK;
                    file_lock.l_start = 0;
                    file_lock.l_whence = SEEK_SET;
                    file_lock.l_len = 0;
                    fcntl(ofdChild, F_SETLK, &file_lock);

                    int cursor = sizeof(double) * N * startIdx + row * sizeof(double) * N + col * sizeof(double);
                    lseek(ofd, cursor, SEEK_SET);
                    Write(ofd, &res[row][col], sizeof(double));

                    // 잠금 해제
                    file_lock.l_type = F_UNLCK;
                    fcntl(ofdChild, F_SETLK, &file_lock);




                }
            }

            // 파일 닫기
            close(ofdChild);
            exit(0);
        }

    }

    int status;
    for (int i = 0; i < childSize; i++) {
        waitpid(-1, &status, 0);
    }

    close_timelog();
    close(ifd1);
    close(ifd2);
    exit(0);
}
