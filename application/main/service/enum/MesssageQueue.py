import enum


class MesssageQueue(enum.Enum):
    Document_classification = 'doc_classify_queue'
    Document_extraction = 'doc_extraction_queue'
