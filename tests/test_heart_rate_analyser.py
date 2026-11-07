import pytest
import allure
from ecg_interpreter.ecg.heart_rate_analyser import (
    analyze_heart_rate,
    average_heart_rate,
    heart_rate_range,
)
from ecg_interpreter.models.interpretation import Diagnosis


@pytest.mark.parametrize(
    "heart_rate, expected",
    [
        (0, Diagnosis.BRADYCARDIA),
        (59.9, Diagnosis.BRADYCARDIA),
        (60, Diagnosis.NORMAL),
        (60.1, Diagnosis.NORMAL),
        (75, Diagnosis.NORMAL),
        (99.9, Diagnosis.NORMAL),
        (100, Diagnosis.NORMAL),
        (100.1, Diagnosis.TACHYCARDIA),
        (300, Diagnosis.TACHYCARDIA),
    ],
)
def test_analyze_heart_rate_valid_values(heart_rate, expected):
    result = analyze_heart_rate(heart_rate)

    assert result == expected, (
        f"При ЧСС {heart_rate} ожидался диагноз {expected.value}, "
        f"получен {result!r}"
    )

@pytest.mark.parametrize(
    "heart_rate, expected_message",
    [
        (None, "не может быть пуст"),
        (-0.1, "не может быть отрицательным"),
        (300.1, "физиологически невозможно"),
        (float("nan"), "должно быть конечным числом"),
    ],
)
def test_analyze_heart_rate_rejects_invalid_values(heart_rate, expected_message):
    with pytest.raises(ValueError, match=expected_message):
        analyze_heart_rate(heart_rate)
@allure.title("Расчёт средней ЧСС по трём измерениям")
def test_average_heart_rate(readings_with_different_heart_rates):
    result = average_heart_rate(readings_with_different_heart_rates)

    assert result == pytest.approx(78.5), (
        f"Для ЧСС 75, 100.5 и 60 ожидалось среднее 78.5, получено {result}"
    )


def test_heart_rate_range(readings_with_different_heart_rates):
    result = heart_rate_range(readings_with_different_heart_rates)

    assert result == (60, 100.5), (
        f"Для ЧСС 75, 100.5 и 60 ожидался диапазон (60, 100.5), получено {result}"
    )


def test_average_heart_rate_rejects_empty_list():
    with pytest.raises(ValueError, match="Список измерений не может быть пустым"):
        average_heart_rate([])


def test_heart_rate_range_rejects_empty_list():
    with pytest.raises(ValueError, match="empty"):
        heart_rate_range([])