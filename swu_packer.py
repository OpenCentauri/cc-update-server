import os, hashlib, subprocess, tempfile, shutil, time, struct

OPENSSL_PATH = os.getenv("OPENSSL_PATH", "openssl")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")
ENCRYPTION_IV = os.getenv("ENCRYPTION_IV", "")

if not ENCRYPTION_KEY or not ENCRYPTION_IV:
    raise ValueError("ENCRYPTION_KEY and IV environment variables must be set")

if hashlib.sha256(ENCRYPTION_KEY.encode()).hexdigest() != "71f1dd02796351fcdcf27e12ae578eec46411234a4a4fcb91d3caa498788c303":
    raise ValueError("Invalid encryption key")

if hashlib.sha256(ENCRYPTION_IV.encode()).hexdigest() != "a4d8ffb1b39dde120a951f27fa71bf99e5435df20196ccd4a131d181a8cda7b6":
    raise ValueError("Invalid IV")

def pack_swu(input_path: str, output_path: str):
    temp_dir = tempfile.TemporaryDirectory()
    root_update_dir = os.path.join(temp_dir.name, "update")
    update_temp_path = os.path.join(root_update_dir, "update")
    os.makedirs(update_temp_path)
    swu_temp_path = os.path.join(update_temp_path, "update.swu")
    shutil.copy(input_path, swu_temp_path)
    zip_temp_path = os.path.join(temp_dir.name, "firmware.zip")
    shutil.make_archive(zip_temp_path.replace('.zip', ''), 'zip', root_update_dir)
    stage1_temp_path = os.path.join(temp_dir.name, "stage1.bin")

    subprocess.run([
        OPENSSL_PATH, 
        "enc", 
        "-aes-256-cbc", 
        "-in", zip_temp_path, 
        "-out", stage1_temp_path,
        "-K", ENCRYPTION_KEY,
        "-iv", ENCRYPTION_IV
    ])

    with open(stage1_temp_path, "rb") as f:
        stage1_data = f.read()

    magic = b"\x14\x17\x0B\x17"
    firmware_info = b"\x01\x01\x2E\x00"
    custom_info = b"\x00\x00\x00\x00"
    firmware_len = struct.pack("<I", len(stage1_data))
    md5_hash = hashlib.md5(stage1_data).digest()

    with open(output_path, "wb") as f:
        f.write(magic)
        f.write(firmware_info)
        f.write(custom_info)
        f.write(firmware_len)
        f.write(md5_hash)
        f.write(stage1_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python swu_packer.py <input.swu> <output.bin>")
        sys.exit(1)

    input_swu = sys.argv[1]
    output_bin = sys.argv[2]

    pack_swu(input_swu, output_bin)