import enum


class WikieditRequestStatus(enum.Enum):
    Completed = 'completed'
    Uploaded = 'uploaded'
    Uploading = 'uploading'
    Pending = 'pending'
    Rejected = 'rejected'
    Cancelled = 'cancelled'
    Accepted = 'accepted'
    Deleted = 'deleted'
