import pytest
from src.main import calculate_heating_index

# Test: HeatingIndex_ShouldBeZero_WhenTemperatureIs20OrAbove
@pytest.mark.parametrize("temperature_in_celsius", [20.0, 21.5, 100.0])
def test_HeatingIndex_ShouldBeZero_WhenTemperatureIs20OrAbove(temperature_in_celsius: float) -> None:
    assert calculate_heating_index(temperature_in_celsius) == 0.0

# Test: HeatingIndex_ShouldBePositive_WhenTemperatureIsBelow20
@pytest.mark.parametrize("temperature_in_celsius,expected", [(19.9, 0.1), (10.0, 10.0), (0.0, 20.0), (-5.0, 25.0)])
def test_HeatingIndex_ShouldBePositive_WhenTemperatureIsBelow20(temperature_in_celsius: float, expected: float) -> None:
    assert calculate_heating_index(temperature_in_celsius) == pytest.approx(expected)