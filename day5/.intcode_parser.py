class IntComputer(object):
    OP_CODES = {
        1: "add",
        2: "multiply",
        3: "input",
        4: "output",
        5: "jump_if_true",
        6: "jump_if_false",
        7: "less_than",
        8: "equals",
        99: "halt"
    }
    INTERMEDIATE_MODE = 1
    POSITION_MODE = 0
    SIMPLE_INPUT = lambda _: 1

    def __init__(self, code, inputs=SIMPLE_INPUT):
        self.code = code
        self.ip = 0
        self.input_idx = 0
        self.inputs = inputs
        self.outputs = []
    
    def __iter__(self):
        return self
    
    def __next__(self):
        assert self.ip < len(self.code), f"{self.ip} {self.code}"
        instr = self.code[self.ip]
        self.run_instr()
        return instr
    
    def run_instr(self):
        try:
            instr = self.code[self.ip]
            opcode = instr % 100
            params = []
            instr //= 100
            while instr:
                params.append(instr % 10)
                instr //=10
            self.ip += 1
            op = getattr(self, IntComputer.OP_CODES[opcode])
        except Exception:
            print(f"opcode={opcode}, params={params}")
            raise
        op(*params)
    
    def get_param(self):
        self.ip += 1
        return self.code[self.ip - 1]
    
    def get_input(self):
        # For diagnostics
        next_input = self.inputs(self.input_idx)
        self.input_idx = self.input_idx + 1
        return next_input

    def add(self, mode1=0, mode2=0, mode3=0):
        assert mode3 == IntComputer.POSITION_MODE
        param1 = self.get_param()
        param2 = self.get_param()
        param3 = self.get_param()
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]
        # print(f"add{mode1, mode2}>", param1, param2, ">>", param3)
        self.code[param3] = param1 + param2

    def multiply(self, mode1=0, mode2=0, mode3=0):
        assert mode3 == IntComputer.POSITION_MODE
        param1 = self.get_param()
        param2 = self.get_param()
        param3 = self.get_param()
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]
        # print(f"mul{mode1, mode2}>", param1, param2, ">>", param3)
        self.code[param3] = param1 * param2

    def jump_if_false(self, mode1=0, mode2=0):
        param1 = self.get_param()
        param2 = self.get_param()
        
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]
        
        if not param1:
            self.ip = param2

    def jump_if_true(self, mode1=0, mode2=0):
        param1 = self.get_param()
        param2 = self.get_param()
        
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]

        if param1:
            self.ip = param2

    def equals(self, mode1=0, mode2=0, mode3=0):
        assert mode3 == IntComputer.POSITION_MODE
        param1 = self.get_param()
        param2 = self.get_param()
        param3 = self.get_param()
        
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]
        if param1:
            self.code[param3] = int(param1 == param2)

    def less_than(self, mode1=0, mode2=0, mode3=0):
        assert mode3 == IntComputer.POSITION_MODE
        param1 = self.get_param()
        param2 = self.get_param()
        param3 = self.get_param()
        
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        if mode2 == IntComputer.POSITION_MODE:
            param2 = self.code[param2]
        if param1:
            self.code[param3] = int(param1 < param2)
    
    def input(self, mode1=0):
        assert mode1 == IntComputer.POSITION_MODE
        param1 = self.get_param()
        # print("input>", param1, self.get_input())
        self.code[param1] = self.get_input()

    def output(self, mode1=0):
        param1 = self.get_param()
        if mode1 == IntComputer.POSITION_MODE:
            param1 = self.code[param1]
        # print(f"output{mode1}>", param1)
        self.outputs.append(param1)
    
    def halt(self):
        raise StopIteration
