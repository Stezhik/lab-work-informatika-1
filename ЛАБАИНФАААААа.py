
s = input()
#перевожу строку в список отдельных токенов (лексер)
token = []
chislo = ''
i = 0
while i < len(s):
    if s[i] in '0123456789' or s[i] == '.':
        chislo += s[i]
        i += 1    #посимвольный сбор числа 

    elif s[i:i+3] == 'log': #ищем логарифм
        if chislo != '':
            token += [chislo]
            chislo = ''
        token += ['log'] #название как отдельный токен
        i += 3            #поэтому пропускам три символа

    elif s[i:i+2] == '>=': #ищем знак больше или равно
        if chislo != '':
            token += [chislo]
            chislo = ''
        token += ['>=']
        i += 2

    elif s[i] in '+-*/()':
        if chislo != '':
            token += [chislo]
            chislo = ''
        token += [s[i]]
        i += 1

    elif s[i] == ' ': #пропускаем пробелы
        i += 1

    else:
        print('cheto ne to')
        i += 1

if chislo != '':       #сохраняем последнее число
    token += [chislo]



#числа в числа знаки в строки
for i in range(len(token)):
    if token[i] not in '+-*/()' and token[i]!='>=' and token[i]!='log':
        token[i]=float(token[i])



# Функция для натурального логарифма
def ln(x):
    if x <= 0:
        print('Аргумент логарифма должен быть больше нуля')
        return None
    k = 0          #счетчик количества делений и умножений на 2
    while x >= 2:
        x = x / 2
        k += 1
    while x < 1:
        x = x * 2
        k -= 1
    z = (x - 1) / (x + 1)
    chislo = 0    #накопление суммы
    stepen = z
    n = 1
    while n <= 199:  #вычисляем сумму ряда до 199
        chislo += stepen / n
        stepen *= z * z
        n += 2
    return 2 * chislo + k * 0.6931471805599453 #приближенное значение



#находим отриц числа и скобочки и логарифм
pos=0
def factor():
    global pos
    if token[pos] == '-':
        pos += 1
        return -factor() #меняем знак результата

    elif token[pos] == '+':
        pos += 1
        return factor() #не меняем знак

    elif token[pos] == 'log':      #с логарифмом 
        pos += 1
        if token[pos] == '(':
            pos += 1
            chislo = expression() #вычисляем то что в скобках
            if token[pos] == ')':
                pos += 1
                return ln(chislo) #вычисляем логарифм 

    elif token[pos] == '(':       #открывающая без лг
        pos += 1
        chislo = expression()
        if token[pos] == ')':
            pos += 1
            return chislo
    else:                      #обычное число
        chislo = token[pos]
        pos += 1
        return chislo



#функция для умножения и деления вызывающая фактор
def term():
    global pos
    chislo=factor()
    while pos<len(token) and token[pos] in '*/':
        znak=token[pos]
        pos+=1
        vtoroe=factor()
        if znak=='*':
            chislo=chislo*vtoroe
        else:
            chislo=chislo/vtoroe
    return chislo



#функция для сложения и вычитания
def expression():
    global pos
    chislo=term()
    while pos<len(token) and token[pos] in '+-':
        znak=token[pos]
        pos+=1
        vtoroe=term()
        if znak=='+':
            chislo=chislo+vtoroe
        else:
            chislo=chislo-vtoroe
    return chislo


#функция для сравнения двух выражений
def comparison():
    global pos
    chislo = expression()

    if pos < len(token) and token[pos] == '>=':
        pos += 1
        vtoroe = expression()
        return chislo >= vtoroe

    return chislo


#вывод результата
result = comparison()
if pos == len(token):
    print(result)
else:
    print('cheto ne to')