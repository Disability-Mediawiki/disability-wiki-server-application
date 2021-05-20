import enum


class DocumentStatus(enum.Enum):
    Processing = 'processing'
    Classified = 'classified'
    Completed = 'completed'
    Uploaded = 'uploaded'
    Deleted = 'deleted'
