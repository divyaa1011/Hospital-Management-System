class HMSException(Exception):
    """Base exception for HMS."""
    pass

class PatientNotFound(HMSException):
    """Raised when patient is not found."""
    pass
