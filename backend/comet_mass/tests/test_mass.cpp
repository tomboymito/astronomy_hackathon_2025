#include <gtest/gtest.h>
#include "../src/comet_mass.cpp"

/**
 * Тест базового расчета массы кометы
 */
TEST(CometMassTest, BasicCalculation) {
    double result = calculate_mass(10.0, 1.0, 1.0);
    EXPECT_NEAR(result, 1.23e20, 1e18);  // Проверка с допуском
}

/**
 * Тест граничных значений
 */
TEST(CometMassTest, EdgeCases) {
    // Проверка на очень большом расстоянии
    EXPECT_GT(calculate_mass(15.0, 1e6, 1e6), 0);
    
    // Проверка на отрицательной звездной величине
    EXPECT_GT(calculate_mass(-5.0, 1.0, 1.0), 0);
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}