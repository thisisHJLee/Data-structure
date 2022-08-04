class Stack:
	def __init__(self):
		self.items = []

	def push(self, val):
		self.items.append(val)

	def pop(self):
		try:
			return self.items.pop()
		except IndexError:
			print("Stack is empty")

	def top(self):
		try:
			return self.items[-1]
		except IndexError:
			print("Stack is empty")

	def __len__(self):
		return len(self.items)

	def isEmpty(self):
		return self.__len__() == 0
	
	def size(self):
		return len(self.items)
	
	
def get_token_list(expr):
	token_list = []
	num = ''
	
	new_expr = expr.replace(' ', '') # 공백 제거
	#print(new_expr)
	for token in new_expr:
		if token in '+-*/^()':
			if num != '':
				token_list.append(num)
				num = ''
			token_list.append(token)
		else:
			num += token
	
	if num != '':
		token_list.append(num)
	
	return token_list

	
def infix_to_postfix(token_list):
	opstack = Stack()
	outstack = []

	# 연산자의 우선순위 설정
	prec = {}
	prec['('] = 0
	prec['+'] = 1
	prec['-'] = 1
	prec['*'] = 2
	prec['/'] = 2
	prec['^'] = 3

	for token in token_list:
		if token == '(':
			opstack.push(token)
		elif token == ')':
			while opstack.top() != '(':
				outstack.append(opstack.pop())
			opstack.pop()
		elif token in '+-/*^':
			while (opstack.size() != 0 and prec[token] <= prec[opstack.top()]):
				outstack.append(opstack.pop())
			opstack.push(token)
		else: # operand일 때
			outstack.append(token)

	# opstack 에 남은 모든 연산자를 pop 후 outstack에 append
	while opstack.size() != 0:
		outstack.append(opstack.pop())

	return outstack

	
def compute_postfix(token_list):
	opstack = Stack()
	
	for token in token_list:
		if token in '+-*/^':	# 이항연산자일 때
			op1 = float(opstack.pop())
			op2 = float(opstack.pop())
			if token == '+': opstack.push(op2 + op1)
			elif token == '-': opstack.push(op2 - op1)
			elif token == '*': opstack.push(op2 * op1)
			elif token == '/': opstack.push(op2 / op1)
			elif token == '^': opstack.push(op2 ** op1)
		else: # operand일 때
			opstack.push(token)
	
	return opstack.pop()
	
	
# 아래 세 줄은 수정하지 말 것!
expr = input()
value = compute_postfix(infix_to_postfix(get_token_list(expr)))
print(value)