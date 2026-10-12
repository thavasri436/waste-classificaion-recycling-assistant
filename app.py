from flask import Flask, render_template, request, jsonify
from PIL import Image
from pathlib import Path
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

WASTE_GUIDE = {
    'Plastic': {'bin': 'Dry / recyclable waste', 'advice': 'Rinse containers and check local recycling rules. Avoid mixing plastic with food waste.'},
    'Paper': {'bin': 'Paper recycling', 'advice': 'Keep paper clean and dry. Greasy or food-soiled paper usually belongs in general waste.'},
    'Metal': {'bin': 'Metal recycling', 'advice': 'Empty and rinse cans. Follow local rules for sharp or bulky metal items.'},
    'Glass': {'bin': 'Glass recycling', 'advice': 'Separate glass where accepted. Wrap broken glass safely and follow local disposal guidance.'},
    'Organic': {'bin': 'Wet / compostable waste', 'advice': 'Fruit and vegetable scraps can often be composted. Keep plastic packaging out of compost.'},
    'E-waste': {'bin': 'Authorized e-waste collection', 'advice': 'Do not put electronics or batteries in regular bins. Use an authorized collection point.'},
    'General': {'bin': 'General waste (check local rules)', 'advice': 'This demo could not confidently identify the item. Check the label or your local waste guide.'}
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def demo_classify(filename, image):
    """Simple offline demo classifier, not a trained AI model."""
    name = filename.lower()
    keywords = {
        'E-waste': ['phone', 'mobile', 'laptop', 'battery', 'charger', 'keyboard', 'mouse', 'electronic'],
        'Organic': ['banana', 'apple', 'food', 'leaf', 'leaves', 'vegetable', 'fruit', 'peel', 'compost'],
        'Paper': ['paper', 'cardboard', 'newspaper', 'book', 'carton'],
        'Plastic': ['plastic', 'bottle', 'wrapper', 'bag', 'container'],
        'Metal': ['metal', 'can', 'tin', 'aluminium', 'aluminum', 'steel'],
        'Glass': ['glass', 'jar']
    }
    for category, words in keywords.items():
        if any(word in name for word in words):
            return category, 0.72, 'Filename-based demo match'

    # Very rough color heuristic for demonstration only; it cannot recognize objects.
    try:
        image = image.convert('RGB').resize((40, 40))
        pixels = list(image.getdata())
        r = sum(p[0] for p in pixels) / len(pixels)
        g = sum(p[1] for p in pixels) / len(pixels)
        b = sum(p[2] for p in pixels) / len(pixels)
        if g > r * 1.12 and g > b * 1.08:
            return 'Organic', 0.42, 'Low-confidence color heuristic'
        if max(r, g, b) - min(r, g, b) < 18 and sum((v - 128) ** 2 for v in (r, g, b)) < 5000:
            return 'Metal', 0.35, 'Low-confidence color heuristic'
    except Exception:
        pass
    return 'General', 0.30, 'No confident match'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'Please choose an image first.'}), 400
    file = request.files['image']
    if not file or not file.filename:
        return jsonify({'error': 'Please choose an image first.'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Use a PNG, JPG, JPEG, or WEBP image.'}), 400
    try:
        raw = file.read()
        image = Image.open(io.BytesIO(raw))
        image.verify()
        image = Image.open(io.BytesIO(raw))
    except Exception:
        return jsonify({'error': 'That image could not be opened. Please try another file.'}), 400

    category, confidence, method = demo_classify(secure_filename(file.filename), image)
    guide = WASTE_GUIDE[category]
    return jsonify({
        'category': category,
        'confidence': round(confidence * 100),
        'bin': guide['bin'],
        'advice': guide['advice'],
        'method': method,
        'notice': 'Prototype demo only: this is not a trained image-recognition AI model. Filename and simple color heuristics can be wrong.'
    })


@app.errorhandler(413)
def too_large(_error):
    return jsonify({'error': 'Image is too large. Please use a file smaller than 8 MB.'}), 413


if __name__ == '__main__':
    app.run(debug=True)
