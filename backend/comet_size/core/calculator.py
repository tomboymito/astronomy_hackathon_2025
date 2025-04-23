import numpy as np
from typing import Union

def calculate_diameter(H: Union[float, np.ndarray], 
                      p: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    if np.any(p <= 0) or np.any(p > 1):
        raise ValueError("Альбедо должно быть в диапазоне (0, 1]")
    
    return 1329 / np.sqrt(p) * 10**(-0.2 * H)