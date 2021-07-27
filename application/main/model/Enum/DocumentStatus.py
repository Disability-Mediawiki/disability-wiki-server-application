import enum


class DocumentStatus(enum.Enum):
    Processing = 'processing'
    Classified = 'classified'
    Completed = 'completed'
    Requested = 'requested'
    Uploaded = 'uploaded'
    Deleted = 'deleted'
    Failed = 'failed'
