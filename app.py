from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your own secret key
app.config['UPLOAD_FOLDER'] = 'uploads'            # Directory to save uploads
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # Set max file size to 2MB

# Create the upload form using Flask-WTF
class UploadForm(FlaskForm):
    image = FileField('Upload Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Upload')

# Main route to display the upload form
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        # Get the uploaded file
        file = form.image.data
        filename = secure_filename(file.filename)
        # Save the file to the specified directory
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'File {filename} uploaded successfully', 'success')
        return redirect(url_for('upload_image'))
    return render_template('upload.html', form=form)

if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

