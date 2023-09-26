import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

cap = cv2.VideoCapture("rtsp://amadeus:4510471@192.168.219.104:554/")  # Replace with your RTSP stream URL

@gzip.gzip_page
def video_feed(request):
    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")