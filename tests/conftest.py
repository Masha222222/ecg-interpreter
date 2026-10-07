import pytest

from ecg_interpreter.models.ecg_data import ECGData, Rhythm, STSegment


@pytest.fixture
def normal_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=False,
    )