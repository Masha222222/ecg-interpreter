import pytest

from ecg_interpreter.models.ecg_data import ECGData, Rhythm, STSegment


@pytest.fixture
def base_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=False,
    )


@pytest.fixture
def arrhythmia_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.IRREGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=False,
    )


@pytest.fixture
def ischemia_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.DEPRESSION,
        q_wave=False,
    )


@pytest.fixture
def suspected_infarction_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.ELEVATION,
        q_wave=False,
    )


@pytest.fixture
def infarction_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.ELEVATION,
        q_wave=True,
    )


@pytest.fixture
def previous_infarction_reading():
    return ECGData(
        heart_rate=75,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.NORMAL,
        q_wave=True,
    )

@pytest.fixture
def readings_with_different_heart_rates(base_reading):
    return [
        base_reading,
        ECGData(
            heart_rate=100.5,
            rhythm=Rhythm.REGULAR,
            st_segment=STSegment.NORMAL,
            q_wave=False,
        ),
        ECGData(
            heart_rate=60,
            rhythm=Rhythm.REGULAR,
            st_segment=STSegment.NORMAL,
            q_wave=False,
        ),
    ]

@pytest.fixture
def infarction_with_tachycardia_reading():
    return ECGData(
        heart_rate=120,
        rhythm=Rhythm.REGULAR,
        st_segment=STSegment.ELEVATION,
        q_wave=True,
    )