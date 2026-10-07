import pytest

from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.interpretation import Diagnosis, Urgency


@pytest.mark.parametrize(
    "heart_rate, expected_diagnosis, expected_urgency",
    [
        (0, Diagnosis.BRADYCARDIA, Urgency.PLANNED),
        (59.9, Diagnosis.BRADYCARDIA, Urgency.PLANNED),
        (60, Diagnosis.NORMAL, Urgency.NONE),
        (75, Diagnosis.NORMAL, Urgency.NONE),
        (100, Diagnosis.NORMAL, Urgency.NONE),
        (100.1, Diagnosis.TACHYCARDIA, Urgency.PLANNED),
        (300, Diagnosis.TACHYCARDIA, Urgency.PLANNED),
    ],
)
def test_interpret_ecg_heart_rate(
    normal_reading, heart_rate, expected_diagnosis, expected_urgency
):
    normal_reading.heart_rate = heart_rate

    result = interpret_ecg(normal_reading)

    assert result.diagnosis == expected_diagnosis, (
        f"При ЧСС {heart_rate} ожидался диагноз {expected_diagnosis.value}, "
        f"получен {result.diagnosis!r}"
    )
    assert result.urgency == expected_urgency, (
        f"При ЧСС {heart_rate} ожидалась срочность {expected_urgency.value}, "
        f"получена {result.urgency!r}"
    )