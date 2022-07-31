# Level2 Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![gitpod ss2](https://user-images.githubusercontent.com/41202066/182039980-369be5d9-4e59-494d-85c5-382204bbd054.png)


## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mkbitmanip module here) which takes in three 32-bit inputs ie. *mav_putvalue_src1*, *mav_putvalue_src2*, *mav_putvalue_src3* and 32-bit instruction select input *mav_putvalue_instr* gives 33-bit output *mav_putvalue* with the least significant bit as a valid output check. If an output is valid the least significant bit of *mav_putvalue* is 1 else 0.

The values are assigned to the 31 input ports ie.  *mav_putvalue_src1*, *mav_putvalue_src2*, *mav_putvalue_src3* and 32-bit instruction select input *mav_putvalue_instr* using 
```
# driving the input transaction
dut.mav_putvalue_src1.value = mav_putvalue_src1
dut.mav_putvalue_src2.value = mav_putvalue_src2
dut.mav_putvalue_src3.value = mav_putvalue_src3
dut.EN_mav_putvalue.value = 1
dut.mav_putvalue_instr.value = mav_putvalue_instr
```
where mav_putvalue_src1,mav_putvalue_src2 and mav_putvalue_src3 is used to store 32-bit input values to send to each src input port of the dut.
mav_putvalue_instr is ised to store the instruction code for the dut to perform.
To get the expected output of the dut the model of the dut is used, so that the observed output and expected output can be checked to find bugs in the design.

The if statement is used to compare the dut's output with the expected value. If the expected output and observed output differ, an error is detected and a counter variable starts to count, how many times an error is detected, for each instruction code of the dut.

To raise an assertion error, the assert statement is used for comparing the error counter to 0.
If the design is error free the error counter must have 0 errors, but in this case there are few errors which can be seen from the output.
The following error is seen:
- Fixed Input operands
```
Failed instr=0x40007033
38.00ns INFO     DUT OUTPUT     =0x100000001
38.00ns INFO     EXPECTED OUTPUT=0x1
assert error_counter == 0, "Test Failed for {n} cases".format(n=error_counter)
                     AssertionError: Test Failed for 1 cases
```
- Varied Input operands
```
Failed instr=0x40007033
37.00ns INFO     DUT OUTPUT     =0x1
37.00ns INFO     EXPECTED OUTPUT=0x3
assert error_counter == 0, "Test Failed for {n} cases".format(n=error_counter)
                     AssertionError: Test Failed for 34848 cases
```
## Test Scenario **(Important)**
- Fixed value Test with Varied Instructions:
  - Test src Inputs: ``mav_putvalue_src1=0xea45f207``,  ``mav_putvalue_src2=0xc3985fa2``,`` mav_putvalue_src3=0x9f09f908``
  - Expected Output:``mav_putvalue = 0x508b400b`` 
  - Observed Output in the DUT ``dut.mav_putvalue=0x18400a405``
  - Failing instrucion : ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011``
  - Corresponding Operation ``--ANDN``
 
- Varied value Test with Varied Instructions (Few of the varied instructions are given here):
  - Input sequence 1:
    - Test src Inputs: ``mav_putvalue_src1=0x20000000``,  ``mav_putvalue_src2=0x80000``,`` mav_putvalue_src3=0x8000000``
    - Expected Output:``mav_putvalue = 0x40000001`` 
    - Observed Output in the DUT ``dut.mav_putvalue=0x1``
    - Failing instrucion : ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011``
    - Corresponding Operation ``--ANDN``
  - Input sequence 2:
    - Test src Inputs: ``mav_putvalue_src1=0x20000000``,  ``mav_putvalue_src2=0x80000``,`` mav_putvalue_src3=0x10000000``
    - Expected Output:``mav_putvalue = 0x40000001`` 
    - Observed Output in the DUT ``dut.mav_putvalue=0x1``
    - Failing instrucion : ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011``
    - Corresponding Operation ``--ANDN``
  - Input sequence 3:
    - Test src Inputs: ``mav_putvalue_src1=0x20000000``,  ``mav_putvalue_src2=0x80000``,`` mav_putvalue_src3=0x20000000``
    - Expected Output:``mav_putvalue = 0x40000001`` 
    - Observed Output in the DUT ``dut.mav_putvalue=0x1``
    - Failing instrucion : ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011``
    - Corresponding Operation ``--ANDN``


Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test inputs and analysing the design, we see that in all the tests only for  ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011`` the dut fails. The corresponding operation for this instruction is the ``ANDN`` operation. For both fixed input values test and varied input values test the ``ANDN`` operations emerges as the bug in the design, as the expected output obtained from the model file does not match the output from the dut for this instruction.
All other operations are correct, as the expected output from the model matches the observed output from the dut, for all the tests.

## Verification Strategy
The verification method is divided into two parts, namely a fixed input test with varied instructions and a varied input test with varied instructions.
In the first test input test, three 32-bit random numbers are generated which stays constant throughout the entire test. For checking each instructions possible, a list of possible instruction codes are generated by varying *opcode*, *f3* and *f7* portions of the instruction code. This results in a list of possible instructions. Each of these instruction codes is cross checked with the model given to verify which instructions are working correctly and which are faulty.

For the second test method, ie. varied input value with varied instructions test, each of the instruction codes for the operations given in the model file, is checked with varying input operands for all three 32-bit inputs. The varying inputs are devised such that all the bits of the inputs are checked to detect bugs. The inputs are varied like ``mav_putvalue_src1=0x0``, ``mav_putvalue_src1=0x1``, ``mav_putvalue_src1=0x2``,``mav_putvalue_src1=0x4``, ``mav_putvalue_src1=0x8`` and so on till ``mav_putvalue_src1=0x80000000``. Basically, each bit of the input ports is checked by shifting a single 1 bit towards left until all 32-bit is covered. This is done for all three inputs ie. *mav_putvalue_src1*, *mav_putvalue_src2* and *mav_putvalue_src3*.

For each tests, an error counter is incremented each time a faulty instruction code is detected.
Finally an assert statement checks if the error counter is equal to zero, if false the assert statement raises an assertion error indicating that the dut has failed. The figure below shows the failing tests.

Both these two tests give a faulty instruction code  ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011`` which is the ``--ANDN`` operation. 
The log results of the tests are given in the figure below and more detailed test logs are given in ``test_varied_inputs.log`` and ``test_varied_instr.log`` files.

![image](https://user-images.githubusercontent.com/110148281/181934455-2fd5a71a-5c49-4af6-9159-0dbd1a704d7c.png)


## Is the verification complete ?
Yes.
After running both the tests on the dut, both raises an error for the instruction ``mav_putvalue_instr=0x40007033`` or ``mav_putvalue_instr = 0b01000000000000000111000000110011`` or the ``--ANDN`` instruction.
All other instruction codes runs successfully without any errors.
