import enum


class MesssageQueue(enum.Enum):
    DOCUMENT_CLASSIFICATION = 'doc_classify_queue'
    DOCUMENT_EXTRACTION = 'doc_extraction_queue'
    UPLOAD_WIKIBASE = 'upload_wikibase'
