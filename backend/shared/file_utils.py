from typing import List

def read_txt(file_path: str) -> List[float]:
    try:
        with open(file_path, 'r') as f:
            return [float(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except ValueError:
        raise ValueError(f"Файл {file_path} содержит некорректные данные")