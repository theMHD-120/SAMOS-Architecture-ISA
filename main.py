"""
| in the name of ALLAH |
<<< the SAMOS Architecture >>>
seyed mahdi mahdavi mortazavi (theMHD)
stdNo: 40030490
"""

# >>> Variables >>> ----------------------------------------------------------------------------------------------------
accumulator = 0  # Acc
tempMemory = []  # A temporary memory while getting instructions form file;
mainMemory = []  # details of each line (instruction) that saved in the memory in its current address (index);
theLastResult = []  # the last results of error detection, index of error location (if error detected) and count of acc;


# >>> Functions >>> ----------------------------------------------------------------------------------------------------
# ... validation funcs ........................................................
def is_digit(inpStr):  # a customised isdigit function using .isdigit() method :);
    if inpStr[0] == '+' or inpStr[0] == '-':
        inpStr = inpStr[1:]
    return inpStr.isdigit()


def is_ins_correct(ins, index):  # to checking instruction correctness;
    if ins[0] == '+' or ins[0] == '-':
        if ins[2] == '000':
            if len(ins[3]) <= 5:
                if is_digit(ins[3][:4]):
                    return True
                else:
                    print(f"Error: the last 4 bits in address {index} are not a constant number;")
            else:
                print(f"Error: Length of the the next address (ic) or constant number in address <{index}> is not valid;"
                      f" Its length is <{len(ins[3]) - 1}>;")
        else:
            print("Error: while working only with a constant number, index of global array must be zero (000);")
    else:
        print(f"Error: the character of sign bit in address {index} is invalid; It should be + or -;")
    # -------------------------
    return False


# ... operations funcs ........................................................
def do_load(ic, accu, index):  # ic : instruction counter (=pc)
    if type(mainMemory[ic]) == int:
        accu = mainMemory[ic]
        return [False, accu]
    else:
        print(f"Error: No constant number found in address <{ic}>;")
        return [True, index]


def do_store(ic, accu):
    mainMemory[ic] = accu
    return [False]


def do_calculates(ic, accu, mod, index):
    if type(mainMemory[ic]) == int:
        if mod == 'ADD':
            accu += mainMemory[ic]
        elif mod == 'SUB':
            accu -= mainMemory[ic]
        elif mod == 'MPY':
            accu *= mainMemory[ic]
        elif mod == 'DIV':
            accu //= mainMemory[ic]
        # .........................
        if -9999999999 <= accu <= 9999999999:
            return [False, accu]
        else:
            print(f"Error: acc gets overflow; Count of acc is <{accu}>;")
            return [True, index]
    else:
        print(f"Error: No constant number found in address <{ic}>;")
        return [True, index]


def do_read(ic, index):
    print("Please enter your numeric data:", end=' ')
    strNum = input()
    if is_digit(strNum):
        mainMemory[ic] = int(strNum)
    else:
        print("Error: the entered data is not a constant number;")
        return [True, index]
    # -------------------------
    if -9999999999 <= mainMemory[ic] <= 9999999999:
        return [False]
    else:
        print(f"Error: the entered number is too large; Its count is <{mainMemory[ic]}>;")
        return [True, index]


def do_write(ic, index):  # not complete...
    if type(mainMemory[ic]) == int:
        print(f"Output: The count of address <{ic}> is <<{mainMemory[ic]}>>;")
        return [False]
    elif mainMemory[ic] == ['\n']:
        print(f"Warning: The address <{ic}> is empty;")
        return [False]
    else:
        print(f"Error: No constant number found in address <{ic}>;")
        return [True, index]


# ... main funcs ..............................................................
def initialize_memory():
    for i in range(10000):
        mainMemory.append(['\n'])


def get_instructions():
    codeFile = open("code.txt", "r")
    tempMem = codeFile.readlines()
    codeFile.close()
    return tempMem


def get_parts_of_instructions(tempMem):
    ins = []
    memIndex = 0
    # -------------------------
    for line in tempMem:
        if len(line) > 5:
            ins.append(line[5])
            ins.append(line[6:9])
            ins.append(line[9:12])
            ins.append(line[12:])
        else:
            ins.append('\n')
        # .........................
        mainMemory[memIndex] = ins
        memIndex += 1
        ins = []


def set_constant_numbers():
    for index in range(10000):
        ins = mainMemory[index]  # ins: instruction
        # .........................
        if type(ins) == list and len(ins) > 1 and ins[1] == '000':
            if is_ins_correct(ins, index):
                constNumber = int(ins[3][:4])
            else:
                return [True, index]
            # .........................
            preHome = mainMemory[index - 1]  # previous home of memory;
            if type(preHome) == int or preHome == ['\n'] or preHome[1] == '000' \
                    or preHome[1] == 'HLT' or preHome[1] == 'BRU':
                mainMemory[index] = constNumber
            else:
                print(f"An assignment operation was found between instructions in address <{index}>")
                return [True, index]
    # -------------------------
    return [False]


def do_instructions(acc):  # not completed
    index = 0
    isIndexMoved = False
    insResults = [False]  # results of the current instruction;
    # -------------------------
    while index < 10000:
        ins = mainMemory[index]  # ins: instruction
        if type(ins) == list and len(ins) > 1:
            if is_ins_correct(ins, index):
                pc = int(ins[3][:4])  # pc = program counter (=ic)
            else:
                return [True, index, acc]
            # .........................
            if ins[1] == 'LDA':
                insResults = do_load(pc, acc, index)
            elif ins[1] == 'STO':
                insResults = do_store(pc, acc)
            elif ins[1] == 'ADD':
                insResults = do_calculates(pc, acc, 'ADD', index)
            elif ins[1] == 'SUB':
                insResults = do_calculates(pc, acc, 'SUB', index)
            elif ins[1] == 'MPY':
                insResults = do_calculates(pc, acc, 'MPY', index)
            elif ins[1] == 'DIV':
                insResults = do_calculates(pc, acc, 'DIV', index)
            elif ins[1] == 'HLT' or ins[1] == 'BRU':
                index = pc
                isIndexMoved = True
                if ins[1] == 'HLT':
                    break
            elif ins[1] == 'BMI':
                if acc < 0:
                    index = pc
                    isIndexMoved = True
            elif ins[1] == 'RWD':
                insResults = do_read(pc, index)
            elif ins[1] == 'WWD':
                insResults = do_write(pc, index)
            else:
                print(f"Error: an invalid operand found in address <{index}>;")
                return [True, index, acc]
            # .........................
            if insResults[0]:
                return [True, index, acc]
            elif len(insResults) == 2:
                acc = insResults[1]
            # .........................
        if isIndexMoved:
            isIndexMoved = False
        else:
            index += 1
    # -------------------------
    if len(insResults) == 1:
        insResults.append(acc)
    return insResults


def show_result(theLastIndex):
    print(">>> The last results:")
    if theLastResult[0]:
        print(f"The last count of acc is: {theLastResult[2]};")
        print(f"An error detected in address <<{theLastResult[1]}>>;")
    else:
        print(f"The last count of acc is: {theLastResult[1]};")
        print("No error found and process finished with exit code 0;")
    print("--------------------------------------------------------------------")
    for index in range(theLastIndex):
        print(index, end=' ')
        ins = mainMemory[index]  # ins: instruction
        # .........................
        if type(ins) == list and len(ins) > 1:
            print(ins[0] + ins[1] + ins[2] + ins[3][:4])
        elif type(ins) == int:
            print(ins)
        elif ins == ['\n']:
            print('')


# >>> Main parts >>> ---------------------------------------------------------------------------------------------------
initialize_memory()
tempMemory = get_instructions()
get_parts_of_instructions(tempMemory)
theLastResult = set_constant_numbers()
# --------------------------------------------------
if not theLastResult[0]:
    theLastResult = do_instructions(accumulator)
    if theLastResult[0]:
        show_result(100)
    else:
        show_result(10000)
else:
    print(f"Attention: An error happened while assigning a constant number in address <{theLastResult[1]}>;"
          " So instructions were not executed;")