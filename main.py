from flask import Flask, render_template, redirect, url_for, send_from_directory
from forms import UploadForm
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from datetime import date
import os

UPLOAD_FOLDER = "static/images"
file_url = None
colors = None
count = None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def get_colors(filename):
    img = Image.open(f"{app.config['UPLOAD_FOLDER']}/{filename}", "r")
    img_array = np.array(img)
    values, counts = np.unique(img_array.reshape(-1, img_array.shape[-1]), axis=0, return_counts=True)
    top_colors_index = np.argsort(-counts)[:10]

    top_rgb = values[top_colors_index]
    hex_codes = [rgb_to_hex(*top_rgb[i, :]) for i in range(top_rgb.shape[0])]

    total = np.sum(counts)
    percentages = np.around((counts[top_colors_index]/total) * 100, decimals=2)

    return hex_codes, percentages


@app.route("/display/<filename>")
def get_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/", methods=['GET', 'POST'])
def home():
    global file_url, colors, count

    form = UploadForm()

    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(path)
        file_url = url_for("get_image", filename=filename)
        colors, count = get_colors(filename)

        return redirect(url_for("home", image=file_url, colors=colors, percent=count))

    return render_template("index.html", form=form, image=file_url, colors=colors, percent=count)


@app.context_processor
def inj_copyright():
    return {"year": date.today().year}


if __name__ == "__main__":
    app.run(debug=True)
