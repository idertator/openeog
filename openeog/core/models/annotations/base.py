from openeog.core.models.enums import AnnotationType


class Annotation:
    def __init__(
        self,
        annotation_type: AnnotationType,
        onset: int,
        offset: int,
    ):
        self._annotation_type = annotation_type
        self.onset = onset
        self.offset = offset

    def __str__(self):
        return "{annotation} from {onset} to {offset}".format(
            annotation=self._annotation_type.value,
            onset=self.onset,
            offset=self.offset,
        )

    @property
    def json(self) -> dict:
        return {
            "annotation_type": self._annotation_type.value,
            "onset": self.onset,
            "offset": self.offset,
        }

    @property
    def annotation_type(self) -> AnnotationType:
        return self._annotation_type
