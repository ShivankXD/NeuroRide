from flask import Flask, render_template, request, jsonify, send_file
import os
from main import process_file  # Import the process_file function

app = Flask(__name__)

# Increase upload size limit to 500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# File upload and processing route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Check if the file type is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Only images (png, jpg, jpeg) and videos (mp4, avi, mov) are supported.'}), 400

    try:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the file using your computer vision model
        result = process_file(file_path)

        # Return the result
        if isinstance(result, str):  # Video processing completed
            return jsonify({
                'success': True,
                'message': result,
                'file_path': file_path,
                'file_type': 'video'
            })
        else:  # Image processing completed
            return jsonify({
                'success': True,
                'number_plate': result,
                'file_path': file_path,
                'file_type': 'image'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Excel download route
@app.route('/download_excel')
def download_excel():
    try:
        # Get the latest Excel file
        current_date = datetime.now().strftime('%Y-%m-%d')
        excel_file_path = os.path.join(current_date, f"{current_date}.xlsx")
        
        if not os.path.exists(excel_file_path):
            return jsonify({'error': 'No Excel file found for today.'}), 404
        
        return send_file(excel_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)