from troml.objects import Libraries, Library

DJANGO_LIBRARY = Library(
    name="django",
    classifier_base="Framework :: Django",
    classifier_pattern=r"^Framework :: Django( :: (?P<version>\d+(\.\d+)?))?$",
)
PYTHON_LIBRARY = Library(
    name="python",
    classifier_base="Programming Language :: Python",
    classifier_pattern=r"^Programming Language :: Python( :: (?P<version>\d+(\.\d+)?))?$",
)

SUPPORTED_LIBRARIES = Libraries(
    [
        DJANGO_LIBRARY,
        PYTHON_LIBRARY,
    ]
)
