from astropy.io import fits
from typing import Dict

def read_fits(file_path: str) -> Dict[str, float]:
    try:
        with fits.open(file_path) as hdul:
            header = hdul[0].header
            return {
                'H': header['H_MAG'],
                'p': header['ALBEDO']
            }
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except KeyError as e:
        raise ValueError(f"Отсутствует необходимый параметр в заголовке: {e}")