from flask import Flask, request, send_file
from PIL import Image
import io
import os

app = Flask(__name__)

# অনুমোদিত ফরম্যাট লিস্ট
ALLOWED_FORMATS = ["jpg", "png", "webp", "bmp", "gif", "heic", "svg"]

@app.route("/convert", methods=["POST"])
def convert_image():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]
    output_format = request.form.get("format", "png").lower()

    if output_format not in ALLOWED_FORMATS:
        return {"error": f"Invalid format! Supported: {', '.join(ALLOWED_FORMATS)}"}, 400

    try:
        # Image লোড করা
        img = Image.open(file.stream)
        img = img.convert("RGBA")  # Transparency সাপোর্টের জন্য
        
        # Output Image তৈরি করা
        output_io = io.BytesIO()
        img.save(output_io, format=output_format.upper())
        output_io.seek(0)

        return send_file(output_io, mimetype=f"image/{output_format}", as_attachment=True, download_name=f"converted.{output_format}")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)