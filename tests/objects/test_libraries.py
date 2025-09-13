from troml.config import DJANGO_LIBRARY
from troml.objects import Libraries


def test():
    DJANGO_LIBRARY.set_versions_from_classifiers()

    actual = Libraries()
    actual.add(DJANGO_LIBRARY)

    assert list(actual) == [DJANGO_LIBRARY]

    assert actual.get("django") == DJANGO_LIBRARY
    assert actual.get("Django") == DJANGO_LIBRARY
    assert actual.get("nonexistent") is None

    assert len(actual.libraries) == 1
