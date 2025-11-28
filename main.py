import swu_packer, gh_extract, tempfile, os, time
from flask import Flask, redirect, url_for, request, render_template, send_from_directory

temp_dir = tempfile.TemporaryDirectory()
latest_version = gh_extract.fetch_latest_release("OpenCentauri", "cc-fw-tools")
print(f"Latest version: {latest_version.version}")
swu_path = os.path.join(temp_dir.name, "latest.swu")
bin_path = os.path.join(temp_dir.name, "latest.bin")
latest_version.download_swu(swu_path)
print(f"Downloaded latest SWU version {latest_version.version} to {swu_path}")
swu_packer.pack_swu(swu_path, bin_path)
print(f"Packed SWU to BIN at {bin_path}")

app = Flask(__name__)

@app.route("/latest")
def latest():
    return send_from_directory(temp_dir.name, "latest.bin")

@app.route("/mainboardVersionUpdate/getInfo.do7")
def update():
    version : str = request.args.get("version")

    

    if not version:
        return "Version parameter is required", 400
    
    if version == latest_version.version or version.strip().rstrip("-oc") == latest_version.version:
        return {
            "code": "000000",
            "messages": None,
            "data": {
                "update": False,
                "version": None,
                "packageUrl": None,
                "firmwareType": 0,
                "packageHash": None,
                "updateStrategy": 0,
                "log": None,
                "timeMS": 0,
                "dataInfoId": None
            },
            "success": True
        }
    else:
        return {
            "code": "000000",
            "messages": None,
            "data": {
                "update": True,
                "version": latest_version.version,
                "packageUrl": request.url_root.rstrip("/") + url_for("latest"),
                "firmwareType": 1,
                "packageHash": "055d4c3c3ff97a9aa5d5e9ba0671739e",
                "updateStrategy": 1,
                "log": latest_version.changelog,
                "timeMS": int(time.time() * 1000),
                "dataInfoId": "770b3a5993c04011bcb1c3a23df1fa5a"
            },
            "success": True
        }
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)