import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Set up the directory where uploaded files will be stored.
# Uses the current directory (.) as the base and adds 'uploads' folder.
UPLOAD_FOLDER = os.path.join('.', 'uploads')

# If the uploads directory doesn't exist, create it.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the app to use the defined uploads folder.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define which file extensions are allowed for upload.
app.config['ALLOWED_EXTENSIONS'] = {
    'txt',
    'pdf',
    'docx', 
    'jpg', 
    'png', 
    'jpeg',
    'ppt',
    'doc',
    'xls',
    'xlsx',
    'bmp',
    'tiff',
    'svg',
    'gif'
    }

# Function to check if the uploaded file has an allowed extension.
def allowed_file(filename):
    # Check if there's an extension and if it's in the allowed list.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Converts files to PDF using LibreOffice's command-line interface.
def convert_to_pdf(filepath):
    # The directory to save the converted PDFs, based on app configuration.
    output_dir = app.config['UPLOAD_FOLDER']
    # Path to the LibreOffice executable.
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    # Run the LibreOffice command to convert the file to PDF and save it in the output directory.
    subprocess.run([soffice_path, '--headless', '--convert-to', 'pdf', '--outdir', output_dir, filepath], check=True)
    # Return the new file path with .pdf extension.
    return os.path.splitext(filepath)[0] + '.pdf'

# Prints PDF files using SumatraPDF.
def print_pdf(filepath):
    # Path to the SumatraPDF executable.
    sumatra_path = r"C:\Users\B-Langhammer\AppData\Local\SumatraPDF\SumatraPDF.exe"
    # Run the SumatraPDF command to print the file to the default printer.
    subprocess.run([sumatra_path, '-print-to-default', filepath], check=True)

# Route for displaying the upload form.
@app.route('/')
def upload_form():
    # Render and return the upload form HTML template.
    return render_template('P_upload.html')

# Route to handle file uploads.
@app.route('/uploads', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'document' not in request.files:
            return "No file part", 400
        file = request.files['document']
        # If no file was selected, return an error.
        if file.filename == '' or not allowed_file(file.filename):
            return "No selected file or file type not allowed", 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save the uploaded file to the filesystem.
        file.save(filepath)
        
        # Convert the file to PDF if it's not already a PDF.
        if not filename.lower().endswith('.pdf'):
            try:
                filepath = convert_to_pdf(filepath)
            except subprocess.CalledProcessError as e:
                return f"Failed to convert file to PDF: {e}", 500
        
        # Attempt to print the PDF file.
        try:
            print_pdf(filepath)
            return "File successfully printed", 200
        except subprocess.CalledProcessError as e:
            return f"Failed to print file: {e}", 500
        
    # If it's not a POST request, just render the upload form again.
    return render_template('P_upload.html')

# Main entry point for the application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
