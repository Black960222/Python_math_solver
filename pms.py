from math import sqrt

########################################

# 分左右
def seperate_lr(eq):
	left = []
	right = []
	is_left = True
	temp = ""
	skip = False

	for x in eq:
		if (skip): skip = False ; continue
		if(x == "+"):
			if (is_left):
				left.append(temp)
			else:
				right.append(temp)
			temp = ""
		elif (x == "-"):
			if (is_left):
				left.append(temp)
			else:
				right.append(temp)
			temp = "-"
		elif (x in "><="):
			left.append(temp)
			is_left = False
			if ("<=" in eq or ">=" in eq):
				skip = True
			temp = ""
		else:
			temp += x
	right.append(temp)
	try:
		left.remove("")
	except: pass
	try:
		right.remove("")
	except: pass

	return(left,right)

# 區分常數項和一次項
def deg0_to_int(left,right):
	for x in range(len(left)):
		try: left[x] = float(left[x])
		except: pass
	for x in range(len(right)):
		try: right[x] = float(right[x])
		except: pass
	return(left, right)

# 常數項移至右邊
def move_deg0_to_right(left,right):
	for x in range(len(left)):
		if (type(left[x]) in [int, float]):
			right.append(-left[x])
			left[x] = None
	temp = []
	for x in left:
		if (x != None):
			temp.append(x)
	left = temp
	return (left, right)

#一次項移至左邊
def move_deg1_to_left(left, right):
	for x in range(len(right)):
		if (type(right[x]) not in (int, float)):
			if(right[x][0] == '-'):
				left.append(right[x][1:])
			else:
				left.append('-' + right[x])
			right[x] = None
	temp = []
	for x in right:
		if (x != None):
			temp.append(x)
	right = temp
	return (left, right)

# 等號右側加總
def add_deg0(right):
	sum = 0
	for x in right:
		sum += x
	right = sum
	return(right)

# 整理方程式 --> ax+by=c
def cleanup(eq,variable1,variable2):
		# ax + by = c
		a = b = c = 0
		
		# Equation 1
		left, right = seperate_lr(eq)
		left, right = deg0_to_int(left,right)
		left, right = move_deg0_to_right(left, right)
		left, right = move_deg1_to_left(left, right)
		right = add_deg0(right)
		c = right
		# 等號左側同類項合併
		# Ex: ["3x","2y","4x",'y'] --> a=7, b=3
		for x in left:
			if(variable1 in x):
				temp = x
				temp = temp.replace("{}".format(variable1),'')
				if (temp == ''): temp = 1
				if (temp == '-'): temp = -1
				temp = float(temp)
				a += temp
			if(variable2 in x):
				temp = x
				temp = temp.replace("{}".format(variable2),'')
				if (temp == ''): temp = 1
				if (temp == '-'): temp = -1
				temp = float(temp)
				b += temp
		return(a,b,c)

########################################


# 一元一次方程式/一元一次不等式
def solve_11(eq,varible,equal):

	# 分左右、區分常數項和一次項
	left, right = seperate_lr(eq)
	left, right = deg0_to_int(left,right)

	# 常數項移至右邊
	left, right = move_deg0_to_right(left, right)

	# 一次項移至左邊
	left, right = move_deg1_to_left(left, right)

	# 等號右側加總
	right = add_deg0(right)

	# 等號左側同類項合併
	temp_all = 0
	for i in left:
		temp = ''
		for j in i:
			if (j != varible):
				temp += j
		if (temp == '-'):
			temp = '-1'
		if (temp == ''):
			temp = '1'
		temp = float(temp)
		temp_all += temp


	# 求解
	if (equal == '='):
		try:
			ans = right / temp_all
		except ZeroDivisionError:
			return(None,None)
	else:
		try:
			ans = right / temp_all			
		except ZeroDivisionError:
			return(None,None)
		else:
			if(temp_all < 0):
				if ('<' in equal):
					equal = equal.replace('<','>')
				elif('>' in equal):
					equal = equal.replace('>','<')
	
	if (ans == -0.0):
		ans = 0.0
	ans = round(ans,5)
	ans = str(ans).replace('.0','')
	
	return(ans,equal)


# 二元一次方程式
def solve_21(eq1,eq2,varible1,varible2):
	
	a1, b1, c1 = cleanup(eq1,varible1,varible2)
	a2, b2, c2 = cleanup(eq2,varible1,varible2)

	# 考慮無限多解和無解
	# 無限多解: 兩線重疊
	if((a1/a2) == (b1/b2) == (c1/c2)):
		return(True,True)
	# 無解: 兩線平行
	if((a1/a2) == (b1/b2) != (c1/c2)):
		return(None,None)
	
	# 加減消去法
	# 解x
	b1x = b1 ; b2x = b2
	a1*=b2x; b1*=b2x; c1*=b2x
	a2*=b1x; b2*=b1x; c2*=b1x
	try:
		x = (c1-c2)/(a1-a2)
	except ZeroDivisionError:
		x = 0
	
	# 解y
	a1x = a1 ; a2x = a2
	a1*=a2x; b1*=a2x; c1*=a2x
	a2*=a1x; b2*=a1x; c2*=a1x
	try:
		y = (c1-c2)/(b1-b2)
	except ZeroDivisionError:
		y = 0
	
	for i in str(x):
		if (i == '.'):
			break


	x = round(x,5)
	y = round(y,5)
	x = str(x).replace(".0",'')
	y = str(y).replace(".0",'')

	return(x,y)


# 一元二次方程式
def solve_12(eq,varible):


	# 分左右
	left, right = seperate_lr(eq)
	left, right = deg0_to_int(left,right)

	# 右側項移至左側
	for x in range(len(right)):
		if(type(right[x]) in [int, float]):
			left.append(-right[x])
		else:
			left.append('-' + right[x])

	# 要變成 ax^2+bx+c=0 的型態
	# 將x^2 變成 X
	for x in range(len(left)):
		if("{}^2".format(varible) in str(left[x])):
			left[x] = left[x].replace("{}^2".format(varible),"α")

	
	# 同類項合併
	
	a = 0
	b = 0
	c = 0


	for i in left:
		if (type(i) in [int, float]):
			c += i
			continue
		if (varible in i):
			temp = i
			temp = temp.replace(varible,'')
			if (temp == ''):
				temp = 1
			b += float(temp)
		if ('α' in i):
			temp = i
			temp = temp.replace('α','')
			if (temp == ''):
				temp = 1
			a += float(temp)
	
	# 公式解
	try:
		x1 = (-b+sqrt(pow(b,2)-4*a*c))/(2*a)
		x2 = (-b-sqrt(pow(b,2)-4*a*c))/(2*a)
		x1 = round(x1,5)
		x2 = round(x2,5)
	except ValueError:
		return(None,None)
	if (x1 == x2):
		return(str(x1).replace(".0",''),None)
	else:
		return(str(x1).replace(".0",''),str(x2).replace(".0",''))
	
