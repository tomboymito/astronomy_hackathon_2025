#include <cmath>
#include <pybind11/pybind11.h>

namespace py = pybind11;

// Константы для расчета массы кометы
const double C1 = -0.4 * (-13.78);  // Константа из формулы (m_лк = -13.78)
const double DENOMINATOR = 1.37e-38 * 0.031;  // Знаменатель формулы (1.37e-38 * f_C2)

/**
 * Расчет массы кометы по заданным параметрам
 * @param m_k Видимая звездная величина кометы
 * @param delta Расстояние от Земли (в а.е.)
 * @param r Расстояние от Солнца (в а.е.)
 * @return Масса кометы (в кг)
 */
double calculate_mass(double m_k, double delta, double r) {
    // Вычисление числителя формулы
    double exponent = -0.4 * m_k + C1;
    double numerator = pow(10, exponent) * delta * delta * r * r;
    
    // Итоговый расчет
    return numerator / DENOMINATOR;
}

// Создание Python-модуля
PYBIND11_MODULE(comet_mass, m) {
    m.def("calculate_mass", &calculate_mass, 
          py::arg("m_k"), py::arg("delta"), py::arg("r"),
          "Расчет массы кометы по формуле Хакатона 2025");
}