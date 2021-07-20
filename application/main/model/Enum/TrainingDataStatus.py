import enum


class TrainingDataStatus(enum.Enum):
    Pending = 'pending'
    Success = 'success'
    Failed = 'failed'
