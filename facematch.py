import face_recognition
from flask import Flask,request,redirect
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file'not in request.files:
             return redirect(request.url)
            
        if 'file1'not in request.files:
             return redirect(request.url)

        file=request.files['file']
        file1=request.files['file1']

        if file.filename=='':
            return redirect(request.url)

        if file1.filename=='':
            return redirect(request.url)
        
        if file and file1 and allowed_file(file.filename)and allowed_file(file1.filename) :
            return detect_faces_in_image(file,file1)
    return '''
    <!doctype html>
    <title>Uploading</title>
    <h1>Upload two pictures to match(jpg/jpeg/png/gif)</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="file" name="file1">
      <input type="submit" value="Upload">
    </form>
    '''

def detect_faces_in_image(file_stream1,file_stream2):
    images1=file_stream1
    images2=file_stream2
    image1=face_recognition.load_image_file(images1)
    image2=face_recognition.load_image_file(images2)
    try:
        encoding1=face_recognition.face_encodings(image1)[0]
    except:
        return("No faces detected in 1st image.Please try uploading a different image.")
    try:
        encoding2=face_recognition.face_encodings(image2)[0]
    except:
        return("No faces detected in 2nd image.Please try uploading a different image.")
    try:
        results=face_recognition.compare_faces([encoding1],encoding2)
        if results[0]:
            return('Same person in both images.')
        else:
            return('Different person in both images.')
    except:
        return("Unable to generate results.")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)

