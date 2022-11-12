from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class UploadForm(FlaskForm):
    image = FileField(
        label="Upload Image",
        validators=[FileRequired(), FileAllowed(['jpg', 'png'], "Images only!")]
    )
    submit = SubmitField("Upload")

