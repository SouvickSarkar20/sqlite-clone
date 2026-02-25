from core.serializer import serialize_row, deserialize_row

def test_serializer():
    # 1. Basic row
    row = {"id": 1, "name": "alice", "age": 25}
    
    # Serialize it
    row_bytes = serialize_row(row)
    print(f"Serialized bytes ({len(row_bytes)} bytes):", row_bytes)
    
    # Deserialize it
    restored_row, bytes_consumed = deserialize_row(row_bytes)
    
    # Verify correctness
    assert restored_row == row, "Restored row doesn't match original!"
    assert bytes_consumed == len(row_bytes), "Mismatch in bytes consumed!"
    
    # 2. Test extraction from a larger buffer (simulating a 4KB page)
    row2 = {"id": 2, "name": "bob", "age": 30}
    row2_bytes = serialize_row(row2)
    
    page_buffer = bytearray(4096)
    
    # Write first row
    page_buffer[0:len(row_bytes)] = row_bytes  # type: ignore
    
    # Write second row right after
    offset = len(row_bytes)
    page_buffer[offset : offset + len(row2_bytes)] = row2_bytes  # type: ignore
    
    # Now read them back in sequence
    read_row1, consumed1 = deserialize_row(page_buffer[0:])  # type: ignore
    assert read_row1 == row
    
    read_row2, consumed2 = deserialize_row(page_buffer[consumed1:])  # type: ignore
    assert read_row2 == row2
    
    # Try reading from empty space
    read_empty, consumed3 = deserialize_row(page_buffer[consumed1 + consumed2:])  # type: ignore
    assert read_empty is None
    assert consumed3 == 0

    print("Serializer test passed!")

if __name__ == "__main__":
    test_serializer()
