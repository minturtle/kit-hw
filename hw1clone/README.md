[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9697793&assignment_repo_type=AssignmentRepo)
# 단일 프로세스로 실행되는 행렬곱 프로그램
This project is written in C, and tested with make and bash scripts.

### The assignment
- 두 이진 파일에서 각각 행렬 A와 행렬 B를 읽어 행렬곱 C를 구한다. 행렬 C를 이진 파일에 저장하는 C 프로그램을 구현한다. 이 프로그램이 읽는 이진 파일은 n\*n double 크기이며, 쓰는 이진 파일도 n\*n double 크기이다. 여기서 n은 1이상의 양수이므로 행렬곱을 수행하는 이 프로그램은 가능한 n\*n 크기의 행렬들을 모두 처리할 수 있어야 한다. 이 프로그램은 3개의 인자를 받는데, 2개의 인자는 입력 이진 파일 이름이고, 세 번째 인자는 출력 이진 파일 이름이다. 세 번째 인자의 이름과 같은 파일이 이미 있으면 덮어쓰기를 한다. 아래 예시에서 data1.bin은 행렬 A의 내용을 담고 있고, data2.bin은 행렬 B의 내용을 담고 있다. res.bin은 행렬곱 결과인 행렬 C의 내용을 담고 있다. 정상적인 실행은 다음과 같으며 0을 반환한다. 

`./hw1 data1.bin data2.bin res.bin`

- 정상적인 실행일 때 프로그램은 별도의 메시지를 출력하지 않고 세 번째 인자에 해당하는 파일만 생성하지만, 에러가 발생하는 경우 다음의 동작을 수행한다.
- hw1이 3개의 인자를 받지 못하면 다음 에러 메시지를 표준에러로 출력하고 1을 반환하며 종료한다.

`Usage: ./hw1 infile1 infile2 outfile`

- 첫 번째 인자 파일의 크기가 n\*n double이 아니면 다음의 에러 메시지를 표준에러로 출력하고 1을 반환하며 종료한다.

`Error: The 1st input file size is not n*n`

- 두 번째 인자 파일의 크기가 첫 번째 인자 파일의 크기와 같지 않으면 다음의 에러 메시지를 표준에러로 출력하고 1을 반환하며 종료한다.

`Error: The 2nd input file size is not the same as the 1st one`

- 제공되는 wrapper.c 코드에는 Open()이나 Creat()와 같은 wrapper 함수들이 제공되며 오류가 있을 경우 1을 반환하며 종료하도록 되어 있다. 이 함수들을 이용하여 코드를 작성한다. 

### Setup command
N/A

### Run command to test program
`make test ARG=1`

`make test ARG=2`

...

`make test ARG=7`

### Notes
- `gcc` can be used to compile and link C applications for use with existing test harnesses or C testing frameworks.
