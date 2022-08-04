class Node:
	def __init__(self, key):
		self.key = key
		self.parent = self.left = self.right = None
		self.height = 0  # 높이 정보도 유지함에 유의!!

	def __str__(self):
		return str(self.key)

class BST:
	def __init__(self):
		self.root = None
		self.size = 0
	def __len__(self):
		return self.size

	def preorder(self, v):
		if v != None:
			print(v.key, end=' ')
			self.preorder(v.left)
			self.preorder(v.right)

	def inorder(self, v):
		if v:
			self.inorder(v.left)
			print(v.key, end = " ")
			self.inorder(v.right)


	def postorder(self, v):
		if v:
			self.postorder(v.left)
			self.postorder(v.right)
			print(v.key, end = " ")

	def find_loc(self, key):
		if self.size == 0: # 빈 트리
			return None
		p = None # p는 v의 부모
		v = self.root
		
		while v != None:
			if v.key == key: return v
			elif v.key < key:
				p = v
				v = v.right
			else:
				p = v
				v = v.left
		return p # 트리에 없는 경우
	
	def search(self, key):
		p = self.find_loc(key)
		if p and p.key == key:
			return p
		else: # 못 찾은 경우
			return None
	
	def updateHeight(self, x):
		while x:
			L = x.left
			R = x.right
			if L and not R:
				x.height = 1 + L.height
			elif not L and R:
				x.height = 1 + R.height
			elif L and R:
				x.height = 1 + max(L.height, R.height)
			else: # x의 자식노드가 없는 경우
				x.height = 0
			x = x.parent

	def insert(self, key):
		# 노드들의 height 정보 update 필요
		# key가 이미 트리에 있다면 에러 출력없이 None만 리턴!
		v = Node(key)
		if self.size == 0: # v가 첫 노드
			self.root = v
		else:
			p = self.find_loc(key)
			if p and p.key != key:
				if p.key >= key:
					p.left = v
				else:
					p.right = v
				v.parent = p
			else: # key가 이미 트리에 있음
				return None
		self.size += 1
		# height 정보 update
		# v.height = 1 + max(self.height(v.left), self.height(v.right))
		self.updateHeight(v)
		return v

	def deleteByMerging(self, x):
		# 노드들의 height 정보 update 필요
		a = x.left
		b = x.right
		pt = x.parent
		# c: x자리를 대체할 노드, m: Left subtree에서 가장 큰 노드
		if a == None:
			c = b
		else: # a != None
			c = m = a
			# a의 subtree에서 m을 찾는다
			while m.right: # 계속 오른쪽 자식노드로
				m = m.right
			m.right = b
			if b: b.parent = m
			# height 정보 update
			# m.height = 1 + max(self.height(m.left), self.height(m.right))
			self.updateHeight(m)
		
		if self.root == x: # c가 새로운 루트노드가 된다
			if c: c.parent = None
			self.root = c
		else: # c가 x의 부모 노드의 자식노드가 된다
			if pt.left == x:
				pt.left = c
			else:
				pt.right = c
			if c: c.parent = pt
			# height 정보 update
			# pt.height = 1 + max(self.height(pt.left), self.height(pt.right))
			self.updateHeight(pt)
		self.size -= 1

	def deleteByCopying(self, x):
		# 노드들의 height 정보 update 필요
		if x == None:
			return None
		
		L = x.left
		R = x.right
		pt = x.parent
		
		if L: # L이 있음
			y = L
			while y.right:
				y = y.right
			x.key = y.key
			if y.left:
				y.left.parent = y.parent
			if y.parent.left is y:
				y.parent.left = y.left
			else:
				y.parent.right =  y.left
			# height 정보 update
			# y.parent.height = 1 + max(self.height(y.parent.left), self.height(y.parent.right))
			self.updateHeight(y)
			del y
		
		elif not L and R: # R만 있음
			y = R
			while y.left:
				y = y.left
			x.key = y.key
			if y.right:
				y.right.parent = y.parent
			if y.parent.left is y:
				y.parent.left = y.right
			else:
				y.parent.right = y.right
			# height 정보 update
			# y.parent.height = 1 + max(self.height(y.parent.left), self.height(y.parent.right))
			self.updateHeight(y.parent)
			del y
		
		else: # L도 R도 없음
			if pt == None: # x가 루트노드인 경우
				self.root = None
			else:
				if pt.left is x:
					pt.left = None
				else:
					pt.right = None
			# height 정보 update
			# pt.height = 1 + max(self.height(pt.left), self.height(pt.right))
			self.updateHeight(pt)
			del x
		self.size -= 1

	def height(self, x): # 노드 x의 height 값을 리턴
		if x == None: return -1
		else: return x.height

	def succ(self, x): # key값의 오름차순 순서에서 x.key 값의 다음 노드(successor) 리턴
		# x의 successor가 없다면 (즉, x.key가 최대값이면) None 리턴
		if x == None: return None
		if x.right: # x의 오른쪽 서브트리가 존재한다면, succ는 x의 오른쪽 서브트리에 존재
			v = x.right
			while v:
				if v.left == None:
					break
				v = v.left
			return v
		else: # x의 오른쪽 서브트리가 존재하지 않는다면, succ는 x의 조상들 중에 존재
			pt = x.parent
			while pt:
				if x != pt.right:
					break;
				x = pt
				pt = pt.parent
			return pt

	def pred(self, x): # key값의 오름차순 순서에서 x.key 값의 이전 노드(predecssor) 리턴
		# x의 predecessor가 없다면 (즉, x.key가 최소값이면) None 리턴
		if x == None: return None
		if x.left: # x의 왼쪽 서브트리가 존재한다면, pred는 x의 오른쪽 서브트리에 존재
			v = x.left
			while v:
				if v.right == None:
					break
				v = v.right
			return v
		else: # x의 왼쪽 서브트리가 존재하지 않는다면, pred는 x의 조상들 중에 존재
			pt = x.parent
			while pt:
				if x != pt.left:
					break;
				x = pt
				pt = pt.parent
			return pt

	def rotateLeft(self, z): # (height 정보 수정 필요)
		if not z: return
		x = z.right
		if x == None: return
		b = x.left
		x.parent = z.parent
		if z.parent:
			if z.parent.right == z:
				z.parent.right = x
			else:
				z.parent.left = x
		x.left = z
		z.parent = x
		z.right = b
		if b: b.parent = z
		if self.root == z and z != None:
			self.root = x
		# height 정보 update
		# z.height = 1 + max(self.height(z.left), self.height(z.right))
		# x.height = 1 + max(self.height(x.left), self.height(x.right))
		self.updateHeight(z)
		self.updateHeight(x)

	def rotateRight(self, z): # (height 정보 수정 필요)
		if not z: return # z가 None
		x = z.left
		if x == None: return
		b = x.right
		x.parent = z.parent
		if z.parent:
			if z.parent.left == z:
				z.parent.left = x
			else:
				z.parent.right = x
		x.right = z
		z.parent = x
		z.left = b
		if b: b.parent =  z # b가 None이 아닌 경우
		if self.root == z and z != None: # z == self.root라면 x가 새로운 root가 됨
			self.root = x
		# height 정보 update
		# z.height = 1 + max(self.height(z.left), self.height(z.right))
		# x.height = 1 + max(self.height(x.left), self.height(x.right))
		self.updateHeight(z)
		self.updateHeight(x)


T = BST()
while True:
	cmd = input().split()
	if cmd[0] == 'insert':
		v = T.insert(int(cmd[1]))
		print("+ {0} is inserted".format(v.key))
	elif cmd[0] == 'deleteC':
		v = T.search(int(cmd[1]))
		T.deleteByCopying(v)
		print("- {0} is deleted by copying".format(int(cmd[1])))
	elif cmd[0] == 'deleteM':
		v = T.search(int(cmd[1]))
		T.deleteByMerging(v)
		print("- {0} is deleted by merging".format(int(cmd[1])))
	elif cmd[0] == 'search':
		v = T.search(int(cmd[1]))
		if v == None:
			print("* {0} is not found!".format(cmd[1]))
		else:
			print("* {0} is found!".format(cmd[1]))
	elif cmd[0] == 'height':
		h = T.height(T.search(int(cmd[1])))
		if h == -1:
			print("= {0} is not found!".format(cmd[1]))
		else:
			print("= {0} has height of {1}".format(cmd[1], h))
	elif cmd[0] == 'succ':
		v = T.succ(T.search(int(cmd[1])))
		if v == None:
			print("> {0} is not found or has no successor".format(cmd[1]))
		else:
			print("> {0}'s successor is {1}".format(cmd[1], v.key))
	elif cmd[0] == 'pred':
		v = T.pred(T.search(int(cmd[1])))
		if v == None:
			print("< {0} is not found or has no predecssor".format(cmd[1]))
		else:
			print("< {0}'s predecssor is {1}".format(cmd[1], v.key))
	elif cmd[0] == 'Rleft':
		v = T.search(int(cmd[1]))
		if v == None:
			print("@ {0} is not found!".format(cmd[1]))
		else:
			T.rotateLeft(v)
			print("@ Rotated left at node {0}".format(cmd[1]))
	elif cmd[0] == 'Rright':
		v = T.search(int(cmd[1]))
		if v == None:
			print("@ {0} is not found!".format(cmd[1]))
		else:
			T.rotateRight(v)
			print("@ Rotated right at node {0}".format(cmd[1]))
	elif cmd[0] == 'preorder':
		T.preorder(T.root)
		print()
	elif cmd[0] == 'postorder':
		T.postorder(T.root)
		print()
	elif cmd[0] == 'inorder':
		T.inorder(T.root)
		print()
	elif cmd[0] == 'exit':
		break
	else:
		print("* not allowed command. enter a proper command!")
