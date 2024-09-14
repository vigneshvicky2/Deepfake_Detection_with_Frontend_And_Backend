from flask import Flask, request, jsonify, render_template, send_file
import os
import tempfile
from main import deepfakespredict , image_predictor 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze')
def Video_detect():
    return render_template('index.html')

@app.route("/upload")
def img_detect():
    return render_template('image.html')


@app.route('/deepfakespredict', methods=['POST'])
def deepfakespredict_endpoint():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400

        video_file = request.files['video']
        
        # Ensure the file is valid
        if not video_file.filename:
            return jsonify({'error': 'Invalid file'}), 400

        # Save the file to a temporary location
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = os.path.join(temp_dir, video_file.filename)
            video_file.save(video_path)

            # Log file details for debugging
            print(f"Received video: {video_path} (Size: {os.path.getsize(video_path)} bytes)")

            # Call your deepfake detection logic
            result_text, confidence_text, video_url = deepfakespredict(video_path)

            return jsonify({
                'resultText': result_text,
                'confidenceText': confidence_text,
                'videoUrl': video_url
            })
    except Exception as e:
        print(f"Error processing the video: {e}")
        return jsonify({'error': 'Internal server error occurred.'}), 500
    
    
@app.route('/imagepredict', methods=['POST'])
def deepfakes_predict():
    if 'image' not in request.files:
        return jsonify({"resultText": "No image uploaded", "confidenceText": ""}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"resultText": "No image selected", "confidenceText": ""}), 400

    # Save the uploaded image temporarily
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, file.filename)
            file.save(image_path)  # Save the image file to the temporary directory

            # Call the image predictor function
            result, image = image_predictor(image_path)  # Process the image here

            # Example response after processing
            return jsonify({"resultText": result, })

    except Exception as e:
        print(f"Error processing the image: {e}")
        return jsonify({"error": "Internal server error occurred."}), 500

if __name__ == '__main__':
    app.run()
