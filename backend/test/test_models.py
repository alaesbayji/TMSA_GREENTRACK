import pytest
from .models import YourModel

@pytest.mark.django_db
def test_model_creation():
    instance = YourModel.objects.create(name="Test")
    assert instance.name == "Test"
