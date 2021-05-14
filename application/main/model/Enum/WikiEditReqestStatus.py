import enum


class WikieditRequestStatus(enum.Enum):
    Completed = 'completed'
    Uploaded = 'uploaded'
    Uloading = 'uploading'
    Pending = 'pending'
    Rejected = 'rejected'
    Cancelled = 'cancelled'
    Deleted = 'deleted'
