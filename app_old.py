from flask import Flask, render_template, request, flash, redirect, session, url_for
from werkzeug.utils import secure_filename
import os, cv2
from main_onetimepredict import predictGLRLMnSVM

app = Flask(__name__)

# Function for
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
UPLOAD_FOLDER = 'static/User/'
GRAY_FOLDER = 'static/User/GRAY'
SEG_FOLDER = 'static/User/SEGMENTATION'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    return render_template('landingPage.html')

@app.route('/identifikasi-kura-kura', methods=['GET', 'POST'])
def uploadPage():
    if request.method == 'POST':
        # print("POST")
        file = request.files['file']
        # print(file)
        if file.filename == '':
            flash('Pilih file nya dulu')
            return redirect(request.url)
            # return ('Hahhh Kosongggggggg')

        if 'file' not in request.files:
            flash('Format file salah')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            if not os.path.isdir(GRAY_FOLDER):
                os.mkdir(GRAY_FOLDER)
            if not os.path.isdir(SEG_FOLDER):
                os.mkdir(SEG_FOLDER)

            filename = secure_filename(file.filename)
            full_filename = os.path.join((UPLOAD_FOLDER), filename)
            gray_filename = os.path.join((GRAY_FOLDER), filename)
            segment_filename = os.path.join((SEG_FOLDER), filename)
            # saveTime = int(time.time())
            # os.makedirs(UPLOAD_FOLDER + '/session/' + str(saveTime) + '/')
            file.save(full_filename)
            predict = predictGLRLMnSVM(full_filename)
            result = predict[0]
            numberofGLRLM = predict[1]

            grayscaleImage = (predict[2])
            # grayscaleImage.save(gray_filename)
            cv2.imwrite(gray_filename, grayscaleImage)

            segmentationImage = (predict[3])
            # segmentationImage.save(segment_filename)
            cv2.imwrite(segment_filename, segmentationImage)


            if result == 'Kura-kura Nanas':
                return render_template('kuraNanas.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Garis Hitam':
                return render_template('kuraGarisHitam.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Batok':
                return render_template('kuraBatok.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Tempurung Datar':
                return render_template('kuraTempurungDatar.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Baning Coklat':
                return render_template('kuraBaningCokelat.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Pipi Putih':
                return render_template('kuraPipiPutih.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Biuku':
                return render_template('kuraBiuku.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            elif result == 'Kura-kura Nanas Muda':
                return render_template('kuraNanasMuda.html', identifikasi='Aktif',
                                       img = full_filename, img_gray = gray_filename, img_segmentation = segment_filename,
                                       SRE = numberofGLRLM[0][0], LRE = numberofGLRLM[0][1], GLU = numberofGLRLM[0][2],
                                       RLU = numberofGLRLM[0][3], RPC = numberofGLRLM[0][4])

            else:
                return redirect(request.url)

            # return result # str(str(filename)+str(full_filename))

    return render_template('uploadPage.html')

@app.route('/informasi')
def infoPage():
    return render_template('informasiKura.html')

@app.route('/tentang')
def aboutPage():
    return render_template('tentangWebsite.html')


@app.route('/Kura-kura-Nanas')
def nanas():
    return render_template('kuraNanas.html')

@app.route('/Kura-kura-Garis-Hitam')
def garishitam():
    return render_template('kuraGarisHitam.html')

@app.route('/Kura-kura-Batok')
def batok():
    return render_template('kuraBatok.html')

@app.route('/Kura-kura-Tempurung-Datar')
def tempurungdatar():
    return render_template('kuraTempurungDatar.html')

@app.route('/Kura-kura-Baning-Cokelat')
def baningcokelat():
    return render_template('kuraBaningCokelat.html')

@app.route('/Kura-kura-Pipi-Putih')
def pipiputih():
    return render_template('kuraPipiPutih.html')

@app.route('/Kura-kura-Biuku')
def biuku():
    return render_template('kuraBiuku.html')

@app.route('/Kura-kura-Nanas-Muda')
def nanasmuda():
    return render_template('kuraNanasMuda.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged innnn')
            return redirect(request.url)
    return render_template('login.html', error=error)

app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # session.init_app(app)
    app.run(debug=True)

# To run on windows
# set FLASK_APP=main_flask.py
# set FLASK_ENV=development