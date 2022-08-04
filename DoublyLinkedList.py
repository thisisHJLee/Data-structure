class Node:
	def __init__(self, key=None):
		self.key = key
		self.prev = self
		self.next = self
	def __str__(self):
		return str(self.key)

class DoublyLinkedList:
	def __init__(self):
		self.head = Node() # create an empty list with only dummy node

	def __iter__(self):
		v = self.head.next
		while v != self.head:
			yield v
			v = v.next
	def __str__(self):
		return " -> ".join(str(v.key) for v in self)

	def printList(self):
		v = self.head.next
		print("h -> ", end="")
		while v != self.head:
			print(str(v.key)+" -> ", end="")
			v = v.next
		print("h")
	# 나머지 코드
	def splice(self, a, b, x): # cut [a..b] after x
		if a == None or b == None or x == None: 
			return
		# 1. [a..b] 구간을 잘라내기 
		a.prev.next = b.next
		b.next.prev = a.prev

		# 2. [a..b]를 x 다음에 삽입하기
		x.next.prev = b
		b.next = x.next
		a.prev = x
		x.next = a

	def moveAfter(self, a, x): # 노드 a를 노드 x 뒤로 이동하기
		self.splice(a, a, x)

	def moveBefore(self, a, x): # 노드 a를 노드 x 앞으로 이동하기
		self.splice(a, a, x.prev)

	def insertAfter(self, a, key): # key 값을 갖는 새 노드 b를 만들어 노드 a 뒤에 삽입
		self.moveAfter(Node(key), a)

	def insertBefore(self, a, key): # 노드 x 앞에 데이터가 key인 새 노드를 생성해 삽입
		self.moveBefore(Node(key), a)

	def pushFront(self, key): # 데이터가 key인 새 노드를 생성해 head 다음(front)에 삽입
		self.insertAfter(self.head, key)

	def pushBack(self, key): # 데이터가 key인 새 노드를 생성해 head 이전(back)에 삽입
		# insertBefore()를 이용할 것
		self.insertBefore(self.head, key)

	def deleteNode(self, x): # 노드 x를 제거
		if x == None or x == self.head:
			return
		# 노드 x를 리스트에서 분리해내기
		x.prev.next, x.next.prev = x.next, x.prev
		del x

	def popFront(self): # head 다음에 있는 노드의 데이터 값 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		key = self.head.next
		self.deleteNode(self.head.next)
		return key

	def popBack(self): # head 이전에 있는 노드의 데이터 값 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		key = self.head.prev
		self.deleteNode(self.head.prev)
		return key

	def search(self, key): #key 값 갖는 노드를 리턴하고, 없으면 None 리턴
		v = self.head
		if key == v.prev.key:
			return v.prev
		while v.next != self.head:
			if v.key == key:
				return v
			v = v.next
		return None # 못 찾은 경우

	def first(self): # 처음 노드를 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		else:
			v = self.head
			return v.next.key

	def last(self): # 마지막 노드를 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		else:
			v = self.head
			return v.prev.key

	def isEmpty(self): # 빈 리스트면 True 아니면 False 리턴
		if self.head.next == self.head: return True
		else: return False
	
	def findMax(self): # 최대 key 값을 찾아 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		v = self.head.next
		max_key = v.key
		while v != self.head:
			if max_key < v.key:
				max_key = v.key
			v = v.next
		return max_key
	
	def deleteMax(self): # 최대 key 값을 삭제하고 그 최대 값을 리턴. 빈 리스트면 None 리턴
		if self.isEmpty(): return None
		max_key = self.findMax()
		v = self.search(max_key)
		self.deleteNode(v)
		return max_key
	
	def sort(self): # 오름차순으로 정렬한 후 정렬된 양방향 리스트를 리턴
		# deleteMax 함수와 pushFront 함수를 이용해서 작성
		L1 = DoublyLinkedList()
		while self.isEmpty() != True:
			max_key = self.deleteMax()
			L1.pushFront(max_key)
		return L1
L = DoublyLinkedList()
while True:
	cmd = input().split()
	if cmd[0] == 'pushF':
		L.pushFront(int(cmd[1]))
		print("+ {0} is pushed at Front".format(cmd[1]))
	elif cmd[0] == 'pushB':
		L.pushBack(int(cmd[1]))
		print("+ {0} is pushed at Back".format(cmd[1]))
	elif cmd[0] == 'popF':
		key = L.popFront()
		if key == None:
			print("* list is empty")
		else:
			print("- {0} is popped from Front".format(key))
	elif cmd[0] == 'popB':
		key = L.popBack()
		if key == None:
			print("* list is empty")
		else:
			print("- {0} is popped from Back".format(key))
	elif cmd[0] == 'search':
		v = L.search(int(cmd[1]))
		if v == None: print("* {0} is not found!".format(cmd[1]))
		else: print("* {0} is found!".format(cmd[1]))
	elif cmd[0] == 'insertA':
		# inserta key_x key : key의 새 노드를 key_x를 갖는 노드 뒤에 삽입
		x = L.search(int(cmd[1]))
		if x == None: print("* target node of key {0} doesn't exit".format(cmd[1]))
		else:
			L.insertAfter(x, int(cmd[2]))
			print("+ {0} is inserted After {1}".format(cmd[2], cmd[1]))
	elif cmd[0] == 'insertB':
		# inserta key_x key : key의 새 노드를 key_x를 갖는 노드 앞에 삽입
		x = L.search(int(cmd[1]))
		if x == None: print("* target node of key {0} doesn't exit".format(cmd[1]))
		else:
			L.insertBefore(x, int(cmd[2]))
			print("+ {0} is inserted Before {1}".format(cmd[2], cmd[1]))
	elif cmd[0] == 'delete':
		x = L.search(int(cmd[1]))
		if x == None:
			print("- {0} is not found, so nothing happens".format(cmd[1]))
		else:
			L.deleteNode(x)
			print("- {0} is deleted".format(cmd[1]))
	elif cmd[0] == "first":
		print("* {0} is the value at the front".format(L.first()))
	elif cmd[0] == "last":
		print("* {0} is the value at the back".format(L.last()))
	elif cmd[0] == "findMax":
		m = L.findMax()
		if m == None:
			print("Empty list!")
		else:
			print("Max key is", m)
	elif cmd[0] == "deleteMax":
		m = L.deleteMax()
		if m == None:
			print("Empty list!")
		else:
			print("Max key", m, "is deleted.")
	elif cmd[0] == 'sort':
		L = L.sort()
		L.printList()
	elif cmd[0] == 'print':
		L.printList()
	elif cmd[0] == 'exit':
		break
	else:
		print("* not allowed command. enter a proper command!")