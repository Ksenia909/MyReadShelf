import enum


class ReadingStatus(str, enum.Enum):
    to_read = "to_read"
    reading = "reading"
    read = "read"
