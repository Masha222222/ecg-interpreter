import pytest
import allure
from ecg_interpreter.models.ecg_data import Rhythm, STSegment
from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.interpretation import Diagnosis, Urgency, Interpretation

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
    base_reading, heart_rate, expected_diagnosis, expected_urgency
):
    base_reading.heart_rate = heart_rate

    result = interpret_ecg(base_reading)
    expected = Interpretation(expected_diagnosis, expected_urgency)

    assert result == expected, (
        f"При ЧСС {heart_rate} ожидалось {expected!r}, "
        f"получено {result!r}"
    )


def test_interpret_ecg_arrhythmia(arrhythmia_reading):
    expected = Interpretation(Diagnosis.ARRHYTHMIA, Urgency.PLANNED)

    result = interpret_ecg(arrhythmia_reading)

    assert result == expected, (
        f"Для аритмии ожидалось {expected!r}, получено {result!r}"
    )


def test_interpret_ecg_ischemia(ischemia_reading):
    expected = Interpretation(Diagnosis.ISCHEMIA, Urgency.PLANNED)

    result = interpret_ecg(ischemia_reading)

    assert result == expected, (
        f"Для ишемии ожидалось {expected!r}, получено {result!r}"
    )


def test_interpret_ecg_suspected_infarction(suspected_infarction_reading):
    expected = Interpretation(Diagnosis.SUSPECTED_INFARCTION, Urgency.URGENT)

    result = interpret_ecg(suspected_infarction_reading)

    assert result == expected, (
        f"Для подозрения на инфаркт ожидалось {expected!r}, получено {result!r}"
    )


def test_interpret_ecg_infarction(infarction_reading):
    expected = Interpretation(Diagnosis.INFARCTION, Urgency.URGENT)

    result = interpret_ecg(infarction_reading)

    assert result == expected, (
        f"Для инфаркта ожидалось {expected!r}, получено {result!r}"
    )


def test_interpret_ecg_previous_infarction(previous_infarction_reading):
    expected = Interpretation(Diagnosis.PREVIOUS_INFARCTION, Urgency.PLANNED)

    result = interpret_ecg(previous_infarction_reading)

    assert result == expected, (
        f"Для перенесённого инфаркта ожидалось {expected!r}, получено {result!r}"
    )
@allure.title("Интерпретация ЭКГ без измерения вызывает ошибку")
def test_interpret_ecg_rejects_missing_reading():
    with pytest.raises(ValueError, match="Данные ЭКГ не могут быть пустыми"):
        interpret_ecg(None)


@pytest.mark.parametrize(
    "heart_rate, expected_message",
    [
        (-0.1, "не может быть отрицательным"),
        (300.1, "физиологически невозможно"),
    ],
)
def test_interpret_ecg_rejects_invalid_heart_rate(
    base_reading, heart_rate, expected_message
):
    base_reading.heart_rate = heart_rate

    with pytest.raises(ValueError, match=expected_message):
        interpret_ecg(base_reading)