def count_unique_numbers(arr):
    unique_numbers = set(arr)
    return len(unique_numbers)

def main():
    # Запросить у пользователя ввод массива чисел
    numbers = []
    print("Введите 9 чисел:")
    for i in range(9):
        num = int(input(f"Число {i+1}: "))
        numbers.append(num)

    # Подсчитать количество уникальных чисел
    unique_count = count_unique_numbers(numbers)

    # Вывести результат
    print(f"Количество уникальных чисел: {unique_count}")

if __name__ == "__main__":
    main()