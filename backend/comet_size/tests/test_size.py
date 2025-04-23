import pytest
import numpy as np
from ..core.calculator import calculate_diameter

def test_normal_values():
    """Тест нормальных значений"""
    assert np.isclose(calculate_diameter(10, 0.04), 1329 / np.sqrt(0.04) * 10**-2)

def test_array_input():
    """Тест с массивом входных данных"""
    H = np.array([10, 15])
    p = np.array([0.04, 0.1])
    expected = np.array([1329 / np.sqrt(0.04) * 10**-2, 
                        1329 / np.sqrt(0.1) * 10**-3])
    assert np.allclose(calculate_diameter(H, p), expected)

def test_invalid_albedo():
    """Тест недопустимых значений альбедо"""
    with pytest.raises(ValueError):
        calculate_diameter(10, 0)  # Альбедо = 0
    with pytest.raises(ValueError):
        calculate_diameter(10, 1.1)  # Альбедо > 1