from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESS_FAILED = "process_failed"
    PROCESSING_SUCCESS = "process_success"
    NO_FILES_ERROR="not_found_files"
    FILE_ID_ERROR="No_file_found_with_this_id"
    PROJECT_NOT_FOUND_ERROR  = "project not found"
    INSERT_INTO_VECTOR_DATBASE_ERROR = 'insert into databese error'
    INSERT_INTO_VECTOR_DATBASE_SUCCESS = 'insert into databese success'
    VECTOR_COLLECTION_RETREIVED = 'VECTOR_COLLECTION_RETREIVED'
    VECTOR_SEARCH_ERROR = "VECTOR_SEARCH_ERROR"
    VECTOR_SEARCH_SUCCESS = "VECTOR_SEARCH_SUCCESS"
    RAG_ANSWER_ERROR = "RAG_ANSWER_ERROR"
    RAG_ANSWER_SUCCESS = "RAG_ANSWER_SUCCESS"