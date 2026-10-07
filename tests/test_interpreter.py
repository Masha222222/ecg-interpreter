import pytest
from ecg_interpreter.models.ecg_data import Rhythm, STSegment
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


@pytest.mark.parametrize(
    "rhythm, st_segment, q_wave, expected_diagnosis, expected_urgency",
    [
        (Rhythm.IRREGULAR, STSegment.NORMAL, False,
         Diagnosis.ARRHYTHMIA, Urgency.PLANNED),

        (Rhythm.REGULAR, STSegment.DEPRESSION, False,
         Diagnosis.ISCHEMIA, Urgency.PLANNED),

        (Rhythm.REGULAR, STSegment.ELEVATION, False,
         Diagnosis.SUSPECTED_INFARCTION, Urgency.URGENT),

        (Rhythm.REGULAR, STSegment.ELEVATION, True,
         Diagnosis.INFARCTION, Urgency.URGENT),

        (Rhythm.REGULAR, STSegment.NORMAL, True,
         Diagnosis.PREVIOUS_INFARCTION, Urgency.PLANNED),
    ],
)
def test_interpret_ecg_other_signs(
    normal_reading, rhythm, st_segment, q_wave,
    expected_diagnosis, expected_urgency
):
    normal_reading.rhythm = rhythm
    normal_reading.st_segment = st_segment
    normal_reading.q_wave = q_wave

    result = interpret_ecg(normal_reading)

    assert result.diagnosis == expected_diagnosis, (
        f"Для ритма {rhythm.value}, ST {st_segment.value}, Q={q_wave} "
        f"ожидался диагноз {expected_diagnosis.value}, "
        f"получен {result.diagnosis!r}"
    )
    assert result.urgency == expected_urgency, (
        f"Для диагноза {expected_diagnosis.value} ожидалась срочность "
        f"{expected_urgency.value}, получена {result.urgency!r}"
    )