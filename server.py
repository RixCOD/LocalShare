import os
import io
import zipfile
import argparse
from flask import Flask, render_template, send_from_directory, send_file, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10 GB max upload

# --- Path Configuration ---
def get_base_path():
    parser = argparse.ArgumentParser(description="Local File Server")
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to a directory OR a single file (e.g. --dir C:\\Videos or --dir C:\\pic.jpg)"
    )
    args, _ = parser.parse_known_args()

    if args.dir:
        return os.path.abspath(args.dir)

    env_dir = os.environ.get("FILE_SERVER_DIR")
    if env_dir:
        return os.path.abspath(env_dir)

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared")

BASE_PATH = get_base_path()
IS_SINGLE_FILE = os.path.isfile(BASE_PATH)

if IS_SINGLE_FILE:
    BASE_DIR = os.path.dirname(BASE_PATH)
    SINGLE_FILE_NAME = os.path.basename(BASE_PATH)
    print(f"[INFO] Single file mode: {BASE_PATH}")
else:
    BASE_DIR = BASE_PATH
    SINGLE_FILE_NAME = None
    if not os.path.exists(BASE_DIR):
        print(f"[INFO] Creating directory: {BASE_DIR}")
        os.makedirs(BASE_DIR)
    else:
        print(f"[INFO] Serving directory: {BASE_DIR}")


@app.route("/")
def index():
    if IS_SINGLE_FILE:
        file_data = [{
            "name": SINGLE_FILE_NAME,
            "is_dir": False,
            "size": os.path.getsize(BASE_PATH)
        }]
    else:
        file_data = []
        for file in sorted(os.listdir(BASE_DIR)):
            path = os.path.join(BASE_DIR, file)
            file_data.append({
                "name": file,
                "is_dir": os.path.isdir(path),
                "size": os.path.getsize(path) if os.path.isfile(path) else "-"
            })

    return render_template("index.html", files=file_data, single_file=IS_SINGLE_FILE)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(BASE_DIR, filename, as_attachment=True)


@app.route("/download-folder/<path:foldername>")
def download_folder(foldername):
    folder_path = os.path.join(BASE_DIR, foldername)
    if not os.path.isdir(folder_path):
        return "Not a folder", 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{foldername}.zip"
    )


@app.route("/upload", methods=["POST"])
def upload():
    if IS_SINGLE_FILE:
        return "Upload not available in single-file mode.", 400

    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    file.save(os.path.join(BASE_DIR, filename))
    print(f"[INFO] Uploaded: {filename}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)