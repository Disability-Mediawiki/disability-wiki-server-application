import enum


class ClassificationResultStatus(enum.Enum):
    Processing = 'processing'
    Updated = 'updated'
    Requested = 'requested'
    Upload_complete = 'upload_complete'
    Deleted = 'deleted'
    Failed = 'failed'
