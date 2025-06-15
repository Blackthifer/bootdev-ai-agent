class Calculator:
    def __init__(self):
        self.operators = {
            "+": (1, lambda a, b: a + b),
            "-": (1, lambda a, b: a - b),
            "*": (2, lambda a, b: a * b),
            "/": (2, lambda a, b: a / b),
        }

    def evaluate(self, expression):
        tokens = expression.strip().split()
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token in self.operators:
                while operator_stack and operator_stack[-1] in self.operators and self.operators[token][0] <= self.operators[operator_stack[-1]][0]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.isdigit() or "." in token:
                output_queue.append(token)
            elif token == "(": operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(": output_queue.append(operator_stack.pop())
                operator_stack.pop()
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack: output_queue.append(operator_stack.pop())

        result_stack = []
        for token in output_queue:
            if token.isdigit() or "." in token:
                result_stack.append(float(token))
            elif token in self.operators:
                operand2 = result_stack.pop()
                operand1 = result_stack.pop()
                operation = self.operators[token][1]
                result = operation(operand1, operand2)
                result_stack.append(result)

        return result_stack[0]