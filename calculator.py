class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, num):
        self.result += num
        return self.result

    def subtract(self, num):
        self.result -= num
        return self.result

    def multiply(self, num):
        self.result *= num
        return self.result

    def divide(self, num):
        if num == 0:
            raise ValueError("0으로 나눌 수 없습니다.")
        self.result /= num
        return self.result

    def clear(self):
        self.result = 0
        return self.result

def main():
    calc = Calculator()
    print(calc.add(5))      # 5
    print(calc.subtract(2)) # 3
    print(calc.multiply(3)) # 9
    print(calc.divide(2))   # 4.5
    print(calc.clear())     # 0

if __name__ == "__main__":
    main()