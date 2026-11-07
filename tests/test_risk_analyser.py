import pytest
import allure
from ecg_interpreter.ecg.risk_analyser import risk_score


@pytest.mark.parametrize(
    "heart_rate, expected",
    [
        (40, 6.0),
        (75, 0.0),
        (120, 6.0),
    ],
)
def test_risk_score_by_heart_rate(base_reading, heart_rate, expected):
    base_reading.heart_rate = heart_rate

    result = risk_score(base_reading)

    assert result == pytest.approx(expected), (
        f"При ЧСС {heart_rate} ожидался риск {expected}, получено {result}"
    )

@allure.title("Расчёт риска при инфаркте с тахикардией")
def test_risk_score_infarction_with_tachycardia(
    infarction_with_tachycardia_reading,
):
    result = risk_score(infarction_with_tachycardia_reading)

    assert result == pytest.approx(32.0), (
        f"Для инфаркта с тахикардией ожидался риск 32.0, получено {result}"
    )


def test_risk_score_rejects_missing_reading():
    with pytest.raises(ValueError, match="Данные ЭКГ не могут быть пустыми"):
        risk_score(None)