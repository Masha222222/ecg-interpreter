import pytest

from ecg_interpreter.ecg.heart_rate_analyser import analyze_heart_rate
from ecg_interpreter.models.interpretation import Diagnosis


@pytest.mark.parametrize(
    "heart_rate, expected",
    [
        (0, Diagnosis.BRADYCARDIA),
        (59.9, Diagnosis.BRADYCARDIA),
        (60, Diagnosis.NORMAL),
        (75, Diagnosis.NORMAL),
        (100, Diagnosis.NORMAL),
        (100.1, Diagnosis.TACHYCARDIA),
        (300, Diagnosis.TACHYCARDIA),
    ],
)
def test_analyze_heart_rate_valid_values(normal_reading, heart_rate, expected):
    normal_reading.heart_rate = heart_rate

    result = analyze_heart_rate(normal_reading.heart_rate)

    assert result == expected, (
        f"При ЧСС {heart_rate} ожидался диагноз {expected.value}, "
        f"получен {result!r}"
    )