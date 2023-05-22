import sys
import json
import instaloader
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from threading import Thread


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.searchButton.clicked.connect(self.thread)
        self.searchButton.clicked.connect(lambda x:  self.commentsList.clear())
        self.saveButton.clicked.connect(self.save_to_txt)
        self.show()

    def get_id(self, link: str):
        id = link.split("/p/")[1].split("/?")[0]
        return id
    
    def get_comments(self):
        data = json.load(open("data.json"))
        L = instaloader.Instaloader()
        L.context.login(data["user_data"]["user_name"], data["user_data"]["password"])
        post_id = self.get_id(self.linkIn.text())
        post = instaloader.Post.from_shortcode(L.context, post_id)
        comments = post.get_comments()
        users = []
        for comment in comments:
            if "@" in comment.text:
                users.append(comment.text.split("@")[1].split(" ")[0])
        count = {}
        for user in users:
            if user in count:
                count[user] += 1
            else:
                count[user] = 1
        sorted_counts = sorted(count.items(), key=lambda x: x[1], reverse=True)
        for chave, valor in sorted_counts:
            self.commentsList.addItem(f"{chave}: {valor}")
    
    def thread(self):
        x = Thread(target=self.get_comments)
        x.start()
    
    def save_to_txt(self):
        with open("users.txt", "w") as f:
            for index in range(self.commentsList.count()):
                item = self.commentsList.item(index)
                f.write(f"{item.text()}\n")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
