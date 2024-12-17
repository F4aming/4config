import csv
import struct
import sys

MEMORY_SIZE = 1024
memory = [0] * MEMORY_SIZE

def load_binary(filename):
    with open(filename, 'rb') as file:
        return file.read()

def execute(binary_data, mem_range, output_file):
    pc = 0
    while pc < len(binary_data):
        opcode = binary_data[pc]
        print(f"PC: {pc}, Opcode: {opcode}, Remaining bytes: {len(binary_data) - pc}")  # Отладочное сообщение

        # Обработка команды LOAD_CONST (6 байт)
        if opcode == 201:  
            if len(binary_data) < pc + 6:
                break
            try:
                # Проверим длину блока для команды
                if len(binary_data) < pc + 6:
                    break

                # Отладка: покажем какие байты считываются
                addr, const = struct.unpack('<HI', binary_data[pc+1:pc+6])

                if addr < MEMORY_SIZE:
                    memory[addr] = const
                else:
                    print(f"Ошибка: адрес {addr} выходит за пределы памяти.")
            except struct.error as e:
                break
            pc += 6

        # Обработка команды LOAD_MEM (5 байт)
        elif opcode == 57:  
            if len(binary_data) < pc + 5:
                print(f"Ошибка: недостаточно данных для команды LOAD_MEM по адресу {pc}. Ожидалось 5 байт, но оставшихся {len(binary_data) - pc} байт.")
                break
            try:
                addr1, addr2 = struct.unpack('<HH', binary_data[pc+1:pc+5])
                if addr1 < MEMORY_SIZE and addr2 < MEMORY_SIZE:
                    memory[addr1] = memory[memory[addr2]]
                    print(f"LOAD_MEM: memory[{addr1}] = memory[memory[{addr2}]] -> {memory[addr1]}")
                else:
                    print(f"Ошибка: один из адресов выходит за пределы памяти.")
            except struct.error as e:
                print(f"Ошибка распаковки для LOAD_MEM по адресу {pc}: {e}")
                break
            pc += 5

        # Обработка команды STORE_MEM (5 байт)
        elif opcode == 27:  
            if len(binary_data) < pc + 5:
                print(f"Ошибка: недостаточно данных для команды STORE_MEM по адресу {pc}. Ожидалось 5 байт, но оставшихся {len(binary_data) - pc} байт.")
                break
            try:
                addr1, addr2 = struct.unpack('<HH', binary_data[pc+1:pc+5])
                if addr1 < MEMORY_SIZE and addr2 < MEMORY_SIZE:
                    memory[memory[addr1]] = memory[addr2]
                    print(f"STORE_MEM: memory[memory[{addr1}]] = memory[{addr2}] -> {memory[memory[addr1]]}")
                else:
                    print(f"Ошибка: один из адресов выходит за пределы памяти.")
            except struct.error as e:
                print(f"Ошибка распаковки для STORE_MEM по адресу {pc}: {e}")
                break
            pc += 5

        # Обработка команды SHR (7 байт)
        elif opcode == 113:  
            if len(binary_data) < pc + 7:
                print(f"Ошибка: недостаточно данных для команды SHR по адресу {pc}. Ожидалось 7 байт, но оставшихся {len(binary_data) - pc} байт.")
                break
            try:
                addr1, addr2, addr3 = struct.unpack('<HHH', binary_data[pc+1:pc+7])
                if addr1 < MEMORY_SIZE and addr2 < MEMORY_SIZE and addr3 < MEMORY_SIZE:
                    if memory[addr3] != 0:
                        memory[addr1] = memory[addr2] >> memory[addr3]
                    else:
                        memory[addr1] = 0  # Предотвращение деления на 0
                    print(f"SHR: memory[{addr1}] = memory[{addr2}] >> memory[{addr3}] -> {memory[addr1]}")
                else:
                    print(f"Ошибка: один из адресов выходит за пределы памяти.")
            except struct.error as e:
                print(f"Ошибка распаковки для SHR по адресу {pc}: {e}")
                break
            pc += 7
        
        else:
            print(f"Неизвестная команда {opcode} по адресу {pc}")
            break
    

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Использование: python interpreter.py <input.bin> <output.csv> <mem_start> <mem_end>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])
    
    binary_data = load_binary(input_file)
    print(f"Размер бинарного файла: {len(binary_data)} байт")  # Отладочное сообщение
    execute(binary_data, (mem_start, mem_end), output_file)
    print("Выполнение завершено. Проверьте файл:", output_file)
