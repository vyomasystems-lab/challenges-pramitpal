# Level1 Design1 Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.
![gitpod ss2](https://user-images.githubusercontent.com/41202066/182040056-bd1beedd-4b9a-4621-840d-6dcfe509a608.png)
## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 31 2-bit inputs ie. *inp0* through *inp30*, 5-bit *sel* input and gives 2-bit output *out*

The values are assigned to the 31 input ports ie. *inp0* through *inp30* using 
```
dut.inp0.value = inputs[0]
dut.inp1.value = inputs[1]
dut.inp2.value = inputs[2]
dut.inp3.value = inputs[3]
.
.
.
dut.inp30.value = inputs[30]
```
where an array inputs[], is used to store 2 bit values to send to each port of the dut.
The if statement is used to compare the mux's output with the expected value. If an error is detected a counter variable starts to count, how many times an error is detected.

The assert statement is used for comparing the error counter to 0.
If the design is error free the error counter must have 0 errors, but in this case there are few errors which can be seen from the output.
The following error is seen:
```
RANDOM VALUE TEST
ERROR!! for Sel= 12,input=3--output=0, is not correct
ERROR!! for Sel= 13,input=1--output=3, is not correct
ERROR!! for Sel= 30,input=3--output=0, is not correct

 assert error_count == 0, "There are {c} errors.".format(c=error_count)
                     AssertionError: There are 3 errors.
FIXED VALUE TEST
ERROR!! for Sel= 12,input=3--output=0, is not correct
ERROR!! for Sel= 30,input=3--output=0, is not correct   

assert error_count == 0, "There are {c} errors.".format(c=error_count)
                     AssertionError: There are 2 errors.
```
## Test Scenario **(Important)**
- Fixed value Test:
- Test Inputs: sel=0b1100, inp12= 0b011 
- Expected Output: out = 0b011 
- Observed Output in the DUT dut.out=0

- Test Inputs: sel=0b11110, inp30= 0b011 
- Expected Output: out = 0b011 
- Observed Output in the DUT dut.out=0

- Random value Test:
- Test Inputs: sel=0b1100, inp12= 0b011 
- Expected Output: out = 0b011 
- Observed Output in the DUT dut.out=0

- Test Inputs: sel=0b1101, inp13= 0b001 
- Expected Output: out = 0b001 
- Observed Output in the DUT dut.out=0b011

- Test Inputs: sel=0b11110, inp30= 0b011 
- Expected Output: out = 0b011 
- Observed Output in the DUT dut.out=0


Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12;//=====>bug
      5'b01101: out = inp13;
```
```
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;
                            //====> bug input30 missing
      default: out = 0;
    endcase
```
For the mux design, the switching statement should be ``5'b01100: out = inp12`` instead of ``5'b01101: out = inp12`` as in the design code and for *inp30* the switching statement is missing which should have been ``5'b11110: out = inp30;``

## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/110148281/181670763-3f9b1bf1-decd-4abc-94e1-606e0ab0bccf.png)


The updated design is checked in as mux.v in *correct_design* directory in *level1_design1*

## Verification Strategy
The verification method is divided into two parts, namely a random input test and a fixed input test.
In the random input test a 64-bit random number is generated. Each 2-bits of that number is then stored in an integer array for 31 inputs of the mux. Thus all the inputs can be checked for random cases of inputs. After asigning the inputs, the *sel* line is iterated from 0 through 30 to check each and every possible outputs, by cross checking its expected output with the observed output.

For the second test method, all the input ports *inp0* through *inp30* are assigned a fixed value of 0b011. After asigning the inputs, the *sel* line is iterated from 0 through 30 to check each and every possible outputs, by cross checking its expected output with the observed output.
For each test an if statement checks if the observed value is same as the expected output, if not a counter is incremented each time an error is detected. 

Finally an assert statement checks if the error counter is equal to zero, if false the assert statement raises an assertion error indicating that the dut has failed. The figure below shows the failing tests.
![image](https://user-images.githubusercontent.com/110148281/181673873-cfe38a9f-b962-4385-8fa1-e6618a602b89.png)

## Is the verification complete ?
Yes.
After correcting the bugs in the design by making some corrections 
both the tests pass with zero errors. Thus the verification is complete and all the bugs are detected.
```
      5'b01011: out = inp11;
      5'b01101: out = inp12;//==>bug
      5'b01100: out = inp12;//corrected
      5'b01101: out = inp13;
```
```
      5'b11100: out = inp28;
      5'b11101: out = inp29;
                            //=> bug input30 missing
      5'b11110: out = inp30; //corrected
      default: out = 0;
```
