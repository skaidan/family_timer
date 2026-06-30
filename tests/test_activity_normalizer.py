import pytest

from apps.backend.app.services.activity_normalizer import ActivityNormalizer


@pytest.fixture
def normalizer():
    return ActivityNormalizer()


def test_normalizes_known_summary(normalizer):
    result = normalizer.normalize({"summary": "Desayuno", "start": 8.0, "end": 9.0})

    assert result["label"] == "Desayuno"
    assert result["icon"] == "🍽️"
    assert result["type"] == "eat"
    assert result["start"] == 8.0
    assert result["end"] == 9.0


def test_normalizes_unknown_summary_to_custom(normalizer):
    result = normalizer.normalize({"summary": "Yoga", "start": 9.0, "end": 10.0})

    assert result["label"] == "Actividad"
    assert result["icon"] == "📌"
    assert result["type"] == "custom"


def test_normalizes_type_priority_over_summary(normalizer):
    result = normalizer.normalize({"summary": "Cena", "type": "work", "start": 19.0, "end": 20.0})

    assert result["label"] == "Trabajo"
    assert result["icon"] == "💼"
    assert result["type"] == "work"
