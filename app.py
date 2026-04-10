from flask import Flask, render_template, request, jsonify, send_file
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def create_booklet(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    pages = list(reader.pages)
    total = len(pages)

    while total % 4 != 0:
        pages.append(PageObject.create_blank_page(
            width=pages[0].mediabox.width,
            height=pages[0].mediabox.height
        ))
        total += 1

    width = float(pages[0].mediabox.width)
    height = float(pages[0].mediabox.height)

    for i in range(0, total, 4):
        p1, p2, p3, p4 = pages[i:i+4]

        # FRONT (2,3)
        front = PageObject.create_blank_page(width=width*2, height=height)
        front.merge_transformed_page(p2, Transformation().translate(0, 0))
        front.merge_transformed_page(p3, Transformation().translate(width, 0))
        writer.add_page(front)

        # BACK (4,1)
        back = PageObject.create_blank_page(width=width*2, height=height)
        back.merge_transformed_page(p4, Transformation().translate(0, 0))
        back.merge_transformed_page(p1, Transformation().translate(width, 0))
        writer.add_page(back)

    with open(output_pdf, "wb") as f:
        writer.write(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["pdf"]

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # unique output file (important)
    output_filename = "booklet_" + file.filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)
    create_booklet(input_path, output_path)

    return jsonify({
        "preview_url": f"/preview/{output_filename}",
        "download_url": f"/download/{output_filename}"
    })

@app.route("/preview/<filename>")
def preview(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path)


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)