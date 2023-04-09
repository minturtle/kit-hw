/* It computes matrix multiplication. Reads two matrix, multiply them, stores the result matrix */
/* Usage: ./hw1 data1.bin data2.bin res.bin */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "wrapper.h"
#include "timeft.h"
#include <math.h>


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



int main(int argc, char *argv[])
{
  if(argc != 4){
    perror("Usage: hw1 infile outfile");
    exit(1);
  }


  // 입력 파일에 대한 기술자
  int ifd1, ifd2, ofd;
  struct stat st_file1;


  // file1에 대한 행렬의 크기 
  int N;
  // file2에 대한 행렬의 크기
  int N2;

  ifd1 = Open(argv[1], O_RDONLY);
  ifd2 = Open(argv[2], O_RDONLY);
  ofd = Creat(argv[3], 0644);


  N = GetMatrixSize(ifd1);
  N2 = GetMatrixSize(ifd2);

  fstat(ifd1, &st_file1);

  if(st_file1.st_size != N * N * sizeof(double)){
    perror("Error: The 1st input file size is not n*n");
    exit(1);
  }

  if(N != N2){
    perror("Error: The 2nd input file size is not the same as the 1st one");
    exit(1);
  }

  
  // 파일의 값을 읽어올 두 행렬
  double ** arr1;
  double ** arr2;
  double ** res;


  arr1 = (double **)malloc(sizeof(double *) * N);
  arr2 = (double **)malloc(sizeof(double *) * N);
  res = (double **)malloc(sizeof(double *) * N);


  for(int i = 0; i < N; i++){
      arr1[i] = (double *)malloc(sizeof(double) * N);
      arr2[i] = (double *)malloc(sizeof(double) * N);
      res[i] = (double *)malloc(sizeof(double) * N);
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


  // 파일 닫기
  close(ifd1);
  close(ifd2);


  // 행렬 곱 계산, 시간 측정 시작
  init_timelog(1);
  start_timelog(0);
  
  
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      res[i][j] = 0.0;
      for (int k = 0; k < N; k++) {
        res[i][j] += arr1[i][k] * arr2[k][j];
      }
    }
  }

  


  // 행렬 곱 계산 완료, 시간 측정 종료 및 출력
  finish_timelog(0);
  close_timelog();
  
  for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            Write(ofd, &res[i][j], sizeof(res[i][j]));
        }
  }
  

  close(ofd);
  return(0);
}
