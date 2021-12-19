def addition(num1, num2):
    return f"[{num1},{num2}]"


def explode_pair(number):
    level = 0
    for pointer, value in enumerate(number):
        if value == "[":
            level += 1
            continue
        elif value == "]":
            level -= 1
            continue
        elif value == "," or level < 5:
            continue

        end = number.index("]", pointer + 1)
        x, y = [int(x) for x in number[pointer:end].split(",")]
        origin = f"[{x},{y}]"

        #Searching number on the left
        for i in range(pointer - 1, -1, -1):
            diff = 0
            if number[i].isdigit():
                from_index = i
                origin_num = number[i]
                for s in range(i, -1, -1):
                    if not number[s].isdigit():
                        origin_num = number[s+1:i+1]
                        from_index = s + 1
                        break
                
                new_number = str(int(origin_num) + x)
                diff = len(new_number) - len(origin_num)
                pointer += diff
                number = number[:from_index] + new_number + number[i+1:]
                break

        #Searching number on the right    
        for j in range(end + diff, len(number)):
            if number[j].isdigit():
                origin_num = number[j]
                for e in range(j, len(number)):
                    if not number[e].isdigit():
                        origin_num = number[j:e]
                        break
                new_number = str(int(origin_num) + y)
                number = number[:j] + new_number + number[j+len(origin_num):]
                break
        origin_index = number.index(origin, pointer - 1)
        origin_end = origin_index + len(origin) - 1
        number = number[:origin_index] + "0" + number[origin_end+1:]
        break

    return number


def split_into_pair(number):
    for index in range(len(number)-1):
        if number[index:index+2].isdigit():
            origin = number[index:index+2]
            if number[index+2].isdigit():
                origin = number[index:index+3]
            num = int(origin)
            first = num // 2
            second = num - first
            result = f"[{first},{second}]"
            end = index + len(origin) - 1
            number = number[:index] + result + number[end+1:]
            break
    return number


def magnitude(number):
    while True:
        before = number
        for i in range(len(number)):
            if not number[i].isdigit():
                continue
            for a in range(i+1, len(number)):
                if not number[a].isdigit():
                    break
            if number[a] != ",":
                continue
            #Check that after comma there is another number
            if not number[a+1].isdigit():
                continue

            bracket_index = number.index("]", a)
            x, y = [int(x) for x in number[i:bracket_index].split(",")]
            origin = f"[{x},{y}]"
            sum = str(3 * x + 2 * y)
            number = number.replace(origin, sum)
            break
        if before == number:
            break
    return number


def calculate_result(puzzle_input):
    number = puzzle_input.pop(0)
    for i in puzzle_input:
        number = addition(number, i)
        while True:
            new_number = explode_pair(number)
            if new_number != number:
                number = new_number
                continue
            new_number = split_into_pair(number)
            if new_number != number:
                number = new_number
                continue
            break
    return number


# Puzzle 1
puzzle_input = []
with open("input.txt", mode="r" ,encoding="utf-8") as file:
    for line in file:
        puzzle_input.append(line.strip())

number = calculate_result(puzzle_input)
result = magnitude(number)
print("Puzzle 1 =", result)


# Puzzle 2
puzzle_input = []
with open("input.txt", mode="r" ,encoding="utf-8") as file:
    for line in file:
        puzzle_input.append(line.strip())

max = 0
for i in range(len(puzzle_input)):
    for j in range(len(puzzle_input)):
        if i == j:
            continue

        numbers = [puzzle_input[i], puzzle_input[j]]
        number = calculate_result(numbers)
        result = magnitude(number)
        if int(result) > max:
            max = int(result)
        
        numbers = [puzzle_input[j], puzzle_input[i]]
        number = calculate_result(numbers)
        result = magnitude(number)
        if int(result) > max:
            max = int(result)

print("Puzzle 2 =", max)