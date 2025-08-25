# vm.py

# Add this class at the top of vm.py
class Frame:
    """Represents a single function call frame."""
    def __init__(self, return_ip):
        self.return_ip = return_ip
        self.variables = {}

class VM:
    def __init__(self, bytecode, functions):
        self.bytecode = bytecode
        self.functions = functions
        self.stack = []
        self.ip = 0
        self.call_stack = [Frame(return_ip=len(bytecode))]

    def current_frame(self): return self.call_stack[-1]

    def run(self):
        while self.ip < len(self.bytecode):
            opcode, arg = self.bytecode[self.ip]
            self.ip += 1

            if opcode == 'PUSH': self.stack.append(arg)
            # --- FIX: Expect word-based opcodes ---
            elif opcode == 'ADD': right, left = self.stack.pop(), self.stack.pop(); self.stack.append(left + right)
            elif opcode == 'SUB': right, left = self.stack.pop(), self.stack.pop(); self.stack.append(left - right)
            elif opcode == 'MUL': right, left = self.stack.pop(), self.stack.pop(); self.stack.append(left * right)
            elif opcode == 'DIV': right, left = self.stack.pop(), self.stack.pop(); self.stack.append(left / right)
            elif opcode == 'COMPARE':
                right, left = self.stack.pop(), self.stack.pop()
                if arg == '==': self.stack.append(left == right)
                elif arg == '!=': self.stack.append(left != right)
                elif arg == '<': self.stack.append(left < right)
                elif arg == '>': self.stack.append(left > right)
            elif opcode == 'JUMP': self.ip = arg
            elif opcode == 'JUMP_IF_FALSE':
                if not self.stack.pop(): self.ip = arg
            elif opcode == 'STORE':
                self.current_frame().variables[arg] = self.stack.pop()
            elif opcode == 'LOAD':
                value = self.current_frame().variables.get(arg)
                if value is None: raise NameError(f"Variable '{arg}' is not defined.")
                self.stack.append(value)
            elif opcode == 'PRINT': print(self.stack.pop())
            elif opcode == 'CALL':
                func_info = self.functions.get(arg)
                if not func_info: raise NameError(f"Function '{arg}' is not defined.")
                new_frame = Frame(return_ip=self.ip)
                for i in range(len(func_info['args'])):
                    new_frame.variables[func_info['args'][-(i+1)]] = self.stack.pop()
                self.call_stack.append(new_frame)
                self.ip = func_info['start_pos']
            elif opcode == 'RETURN':
                return_value = self.stack.pop()
                frame = self.call_stack.pop()
                self.ip = frame.return_ip
                self.stack.append(return_value)
            else:
                raise Exception(f"Unknown opcode {opcode}")