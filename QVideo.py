'''
Author: jason
Date: 2023-09-29 13:56:19
LastEditTime: 2023-11-02 15:24:46
LastEditors: jason
Description: 
'''
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# 视频路径
# video_path='C:\\Users\\anxie\\Desktop\\Qt\\video.MOV'
video_path='video.MOV'

class Video(QWidget):
    def __init__(self):
        super(Video, self).__init__()

        layout=QVBoxLayout(self)

        title = QLabel()
        title.setText("垃圾分类宣传片")
        font = QFont("Arial", 12)
        title.setFont(font)
        title.setStyleSheet(f"color: black")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.video_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.video_player.setVideoOutput(self.video_widget)

        layout.addWidget(self.video_widget)

        self.play_video()
        self.circle_play()

    def play_video(self):
        # 加载视频文件
        media = QMediaContent(QUrl.fromLocalFile(video_path))
        self.video_player.setMedia(media)

        # 检查是否有错误
        if self.video_player.error() != QMediaPlayer.NoError:
            print("播放器错误:", self.video_player.errorString())
            return  # 如果出现错误，不继续播放

        # 播放视频
        self.video_player.play()

    def circle_play(self):
        # 连接 mediaStatusChanged 信号
        self.video_player.mediaStatusChanged.connect(self.handle_media_status)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # 播放结束，重新开始播放
            self.video_player.setPosition(0)
            self.video_player.play()

if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Video()
    w.show()
    print(type(w))
    sys.exit(app.exec_())
