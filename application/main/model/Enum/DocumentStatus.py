import enum


class DocumentStatus(enum.Enum):
    Processing = 'processing'
    Completed = 'completed'
    Uploaded = 'uploaded'
    Deleted = 'deleted'
