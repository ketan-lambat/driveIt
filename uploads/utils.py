import os
import tempfile
import hashlib

from base64 import b64encode as encode_base64


def encode_base64_to_string(data):
    """
    Helper to encode a string or bytes value to a base64 string as bytes
    """
    if isinstance(data, str):
        data = bytes(data, "utf-8")
    return encode_base64(data).decode("ascii").rstrip("\n")


def encode_upload_metadata(upload_metadata):
    """
    Encodes upload metadata according to the TUS 1.0.0 spec
    (http://tus.io/protocols/resumable-upload.html#creation)
    :param dict upload_metadata:
    :return str:
    """
    # Prepare encoded data
    encoded_data = [
        (key, encode_base64_to_string(value))
        for (key, value) in sorted(
            upload_metadata.items(), key=lambda item: item[0]
        )
    ]

    # Encode into string
    return ",".join(
        [" ".join([key, encoded_value]) for key, encoded_value in encoded_data]
    )


def write_bytes_to_file(file_path, offset, data, makedirs=False):
    """
    Util to write bytes to a local file at a specific offset

    :param str file_path:
    :param int offset:
    :param bytes data:
    :param bool makedirs: Whether or not to create the file_path's
           directories if they don't exist
    :return int: The amount of bytes written
    """
    if makedirs:
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

    num_bytes_written = -1

    fh = None
    try:
        try:
            fh = open(file_path, "r+b")
        except IOError:
            fh = open(file_path, "wb")
        fh.seek(offset, os.SEEK_SET)
        num_bytes_written = fh.write(data)
    finally:
        if fh is not None:
            fh.close()

    return num_bytes_written


def read_bytes_from_field_file(field_file):
    """
    Returns the bytes read from a FieldFile

    :param ~django.db.models.fields.files.FieldFile field_file:
    :return bytes: bytes read from the given field_file
    """
    try:
        field_file.open()
        result = field_file.read()
    finally:
        field_file.close()
    return result


def read_bytes(path):
    """
    Returns the bytes read from a local file at the given path

    :param str path: The local path to the file to read
    :return bytes: bytes read from the given field_file
    """
    with open(path, "r+b") as fh:
        result = fh.read()
    return result


def write_chunk_to_temp_file(data):
    """
    Write some bytes to a local temporary file and return the path

    :param bytes data: The bytes to write
    :return str: The local path to the temporary file that has been written
    """
    fd, chunk_file = tempfile.mkstemp(prefix="tus-upload-chunk-")
    os.close(fd)

    with open(chunk_file, "wb") as fh:
        fh.write(data)

    return chunk_file


def create_checksum(data, checksum_algorithm):
    """
    Create a hex-checksum for the given bytes using the given algorithm

    :param bytes data: The bytes to create the checksum for
    :param str checksum_algorithm: The algorithm to use (e.g. "md5")
    :return str: The checksum (hex)
    """
    m = hashlib.new(checksum_algorithm)
    m.update(data)
    return m.hexdigest()


def create_checksum_header(data, checksum_algorithm):
    """
    Creates a hex-checksum header for the given bytes using the given algorithm

    :param bytes data: The bytes to create the checksum for
    :param str checksum_algorithm: The algorithm to use (e.g. "md5")
    :return str: The checksum algorithm, followed by the checksum (hex)
    """
    checksum = create_checksum(data, checksum_algorithm)
    return "{checksum_algorithm} {checksum}".format(
        checksum_algorithm=checksum_algorithm, checksum=checksum
    )


def checksum_matches(checksum_algorithm, checksum, data):
    """
    Checks if the given checksum matches the checksum for the data in the file

    :param str checksum_algorithm: The checksum algorithm to use
    :param str checksum: The original hex-checksum to match against
    :param bytes data: The bytes to check
    :return bool: Whether or not the newly calculated checksum matches the
                  given checksum
    """
    bytes_checksum = create_checksum(data, checksum_algorithm)
    return bytes_checksum == checksum
