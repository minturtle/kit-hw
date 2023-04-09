diff_max=0.00001

function missed_arg() {
    $1 $2 $3 $4 $5 2> temp.txt
    if [ $? -eq 0 ] ; then
	echo "Fail: Program should use 3 args"
	exit 1
    fi
    output=$(cat temp.txt)    
    if [ -z "${output}" ] ; then
	echo "Fail: No error message for incorrent arguments"
	exit 1
    fi        
    if [[ "${output}" != *"Usage"* ]] && [[ "${output}" != *"hw1"* ]] && [[ "${output}" != *"infile"* ]] ; then
	echo "Fail: Incorrect error message(${output})"
	exit 1
    fi
}
    
function missed_arg_test() {
    missed_arg "./hw1"
    
    missed_arg "./hw1 data1.bin"

    missed_arg "./hw1 data1.bin data2.bin"

    missed_arg "./hw1 data1.bin data2.bin res.bin res2.bin"
}

function square_test() {
    ./hw1 notsq57.bin id3.bin res.bin 2> temp.txt
    if [ $? -eq 0 ] ; then
	echo "Fail: Program cannot detect not square matrix file"
	exit 1
    fi
    output=$(cat temp.txt)
    if [ -z "${output}" ] ; then
	echo "Fail: No error message for incorrent arguments"
	exit 1
    fi        
    if [[ "${output}" != *"file"* ]] && [[ "${output}" != *"size"* ]] && [[ "${output}" != *"not"* ]] && [[ "${output}" != *"n*n"* ]] ; then
	echo "Fail: Incorrect error message(${output}) for not square matrix file."
	exit 1
    fi
}

function file_size_t() {
    $1 $2 $3 2> temp.txt
    if [ $? -eq 0 ] ; then
	echo "Fail: Program cannot detect different file sizes"
	exit 1
    fi
    output=$(cat temp.txt)
    if [ -z "${output}" ] ; then
	echo "Fail: No error message for incorrent arguments"
	exit 1
    fi        
    if [[ "${output}" != *"file"* ]] && [[ "${output}" != *"size"* ]] && [[ "${output}" != *"not"* ]] && [[ "${output}" != *"same"* ]] ; then
	echo "Fail: Incorrect error message(${output}) for different file size."
	exit 1
    fi
}

function file_size_test() {
    file_size_t "./hw1 data1.bin id3.bin res.bin"

    file_size_t "./hw1 rand31.bin rand100.bin res.bin"
}

function basic_1x1_test(){ 
    output=$(./hw1 data1.bin data2.bin res.bin)
    if [ $? -eq 0 ] ; then
	echo "Pass: (1*1) Program exited zero"
    else
	echo "Fail: (1*1) Program did not exit zero"
	exit 1
    fi

    outputd=$(./hwdiffd res.bin data3.bin ${diff_max})
    if [ $? -eq 0 ] ; then
	echo "Pass: (1*1) Output is correct"
    else
	echo "Fail: (1*1) Output is not expected result"
	exit 1
    fi
}

function nxn_test(){
    output=$(./hw1 rand$1.bin inv_rand$1.bin res.bin)
    if [ $? -eq 0 ] ; then
	echo "Pass: ($1*$1) Program exited zero"
    else
	echo "Fail: ($1*$1) Program did not exit zero"
	exit 1
    fi

    outputd=$(./hwdiffd res.bin id$1.bin ${diff_max})
    if [ $? -eq 0 ] ; then
	echo "Pass: ($1*$1) Output is correct"
    else
	echo "Fail: ($1*$1) Output is not expected result"
	exit 1
    fi
}

function idxn_test(){
    output=$(./hw1 rand$1.bin id$1.bin res.bin)
    if [ $? -eq 0 ] ; then
	echo "Pass: (id$1*rand$1) Program exited zero"
    else
	echo "Fail: (id$1*rand$1) Program did not exit zero"
	exit 1
    fi

    outputd=$(./hwdiffd res.bin rand$1.bin ${diff_max})
    if [ $? -eq 0 ] ; then
	echo "Pass: (id$1*rand$1) Output is correct"
    else
	echo "Fail: (id$1*rand$1) Output is not expected result"
	exit 1
    fi
}

echo "Running tests..."
echo

case $1 in
    "1") missed_arg_test;;
    "2") square_test;;
    "3") file_size_test;;
    "4") basic_1x1_test;;
    "5") nxn_test "31";;
    "6") nxn_test "1000";;
    "7") idxn_test "1000";;
    *) echo "Invalid argument ($1) for the script"
       exit 1;;
esac

echo "Test $1 passed."
exit 0
