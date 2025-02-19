import os, time

# Generate 10MB
data_len = 10000000
data = os.urandom(data_len)
file_ct = 1000
file_len = int(data_len/file_ct)

# Write one large file
start = time.perf_counter()
large_file = open("large.bin", "wb")
large_file.write(data)
large_file.close ()
large_write_s = time.perf_counter() - start

# Write multiple small files
start = time.perf_counter()
for i in range(file_ct):
    small_file = open(f"small_{i}.bin", "wb")
    small_file.write(data[file_len*i:file_len*(i+1)])
    small_file.close()
small_write_s = time.perf_counter() - start

# Read back the large file
start = time.perf_counter()
large_file = open("large.bin", "rb")
t = large_file.read(data_len)
large_file.close ()
large_read_s = time.perf_counter() - start

# Read back the small files
start = time.perf_counter()
for i in range(file_ct):
    small_file = open(f"small_{i}.bin", "rb")
    t = small_file.read(file_len)
    small_file.close()
small_read_s = time.perf_counter() - start

# Print Summary
print(f"{1:5d}x{data_len/1000000}MB Write: {large_write_s:.5f} seconds")
print(f"{file_ct:5d}x{file_len/1000}KB Write: {small_write_s:.5f} seconds")
print(f"{1:5d}x{data_len/1000000}MB Read: {large_read_s:.5f} seconds")
print(f"{file_ct:5d}x{file_len/1000}KB Read: {small_read_s:.5f} seconds")
print(f"{file_ct:5d}x{file_len/1000}KB Write was {small_write_s/large_write_s:.1f} slower than 1x{data_len/1000000}MB Write")
print(f"{file_ct:5d}x{file_len/1000}KB Read was {small_read_s/large_read_s:.1f} slower than 1x{data_len/1000000}MB Read")

# Cleanup
os.remove("large.bin")
for i in range(file_ct):
    os.remove(f"small_{i}.bin")