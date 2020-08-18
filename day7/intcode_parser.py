class defaultlist(list):
    def __init__(self, fx):
        self._fx = fx
    def _fill(self, index):
        while len(self) <= index:
            self.append(self._fx())
    def __setitem__(self, index, value):
        self._fill(index)
        list.__setitem__(self, index, value)
    def __getitem__(self, index):
        self._fill(index)
        return list.__getitem__(self, index)

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
        9: "adjust_base",
        99: "halt",
    }
    RELATIVE_MODE = 2
    INTERMEDIATE_MODE = 1
    POSITION_MODE = 0
    SIMPLE_INPUT = lambda _: 1

    def __init__(self, code, inputs=SIMPLE_INPUT):
        self.code = defaultlist(int)
        self.code.extend(code)
        self.ip = 0
        self.input_idx = 0
        self.inputs = inputs
        self.outputs = []
        self.relative_base = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        assert self.ip < len(self.code), f"{self.ip} {self.code}"
        instr = self.code[self.ip]
        self.run_instr()
        return instr
    
    def run_instr(self):
        opcode, params = None, None
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
    
    def get_param(self, mode=INTERMEDIATE_MODE):
        self.ip += 1
        param = self.code[self.ip - 1]
        if mode == IntComputer.INTERMEDIATE_MODE:
            return param
        if mode == IntComputer.POSITION_MODE:
            return self.code[param]
        if mode == IntComputer.RELATIVE_MODE:
            return self.code[param + self.relative_base]
    
    def set_value(self, val, mode=POSITION_MODE):
        assert mode in {IntComputer.POSITION_MODE, IntComputer.RELATIVE_MODE}
        param = self.get_param(mode=IntComputer.INTERMEDIATE_MODE)
        if mode == IntComputer.RELATIVE_MODE:
            param += self.relative_base
        self.code[param] = val 

    
    def get_input(self):
        # For diagnostics
        next_input = self.inputs(self.input_idx)
        self.input_idx = self.input_idx + 1
        return next_input

    def add(self, mode1=0, mode2=0, mode3=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)
        # print(f"add{mode1, mode2}>", param1, param2, ">>", param3)
        self.set_value(param1 + param2, mode=mode3)

    def multiply(self, mode1=0, mode2=0, mode3=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)

        # print(f"mul{mode1, mode2}>", param1, param2, ">>", param3)
        self.set_value(param1 * param2, mode=mode3)

    def jump_if_false(self, mode1=0, mode2=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)
        
        if not param1:
            self.ip = param2

    def jump_if_true(self, mode1=0, mode2=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)

        if param1:
            self.ip = param2

    def equals(self, mode1=0, mode2=0, mode3=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)

        if param1:
            self.set_value(int(param1 == param2), mode=mode3)
        else:
            self.get_param()

    def less_than(self, mode1=0, mode2=0, mode3=0):
        param1 = self.get_param(mode1)
        param2 = self.get_param(mode2)

        if param1:
            self.set_value(int(param1 < param2), mode=mode3)
        else:
            self.get_param()
    
    def input(self, mode1=0):
        inp = self.get_input()
        print(f"[COMP] inp={inp}")
        self.set_value(inp, mode=mode1)

    def output(self, mode1=0):
        param1 = self.get_param(mode1)
        # print(f"output{mode1}>", param1)
        self.outputs.append(param1)
    
    def adjust_base(self, mode1=0):
        param1 = self.get_param(mode1)
        self.relative_base += param1

    def halt(self):
        raise StopIteration
