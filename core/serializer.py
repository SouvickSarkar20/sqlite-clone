import json
import struct

def serialize_row(row_dict):
    """
    Converts a Python dictionary to a length-prefixed byte sequence.
    Format: [2 bytes: length of payload] [N bytes: JSON payload]
    """
    # Convert dict to JSON string, then to utf-8 bytes
    payload = json.dumps(row_dict, separators=(',', ':')).encode('utf-8')
    
    # Calculate length and pack it into a 2-byte unsigned short (big-endian)
    # '>H' stands for unsigned short (2 bytes), big-endian
    length_prefix = struct.pack('>H', len(payload))
    
    return length_prefix + payload

def deserialize_row(data_bytes):
    """
    Converts a length-prefixed byte sequence back to a Python dictionary.
    Returns: (row_dict, bytes_consumed)
    If the data is invalid or empty, returns (None, 0).
    """
    if len(data_bytes) < 2:
        return None, 0
        
    # Unpack the 2-byte length prefix
    payload_len = struct.unpack('>H', data_bytes[:2])[0]
    
    # Check if we have enough bytes for the full payload, or if length is 0 (empty data)
    if payload_len == 0 or len(data_bytes) < 2 + payload_len:
        return None, 0
        
    # Extract payload and parse JSON
    payload = data_bytes[2 : 2 + payload_len]
    try:
        row_dict = json.loads(payload.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # In case we read garbage data from an empty page
        return None, 0
    
    # Return the dictionary and how many bytes this row took in total
    bytes_consumed = 2 + payload_len
    return row_dict, bytes_consumed
