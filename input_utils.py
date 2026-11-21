def input_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            raw = input(prompt).strip()

            if not raw:
                print(f"빈칸은 입력할 수 없습니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue

            value = int(raw)

            if value < min_value or value > max_value:
                print(f"범위를 벗어났습니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

        except ValueError:
            print(f"숫자만 입력할 수 있습니다. {min_value}~{max_value} 사이의 숫자를 입력하세요.")
        except KeyboardInterrupt:
            raise


def input_non_empty(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("내용을 비워둘 수 없습니다. 다시 입력하세요.")
