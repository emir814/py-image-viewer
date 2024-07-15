import sys
from PyQt5.QtCore import Qt, QRectF, QSettings
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QMainWindow

class ImageViewer(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap(image_path)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmap_item)

        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(Qt.black)
        self.setStyleSheet("background:black;")
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMinimumSize(300, 300)

    def resizeEvent(self, event):
        self.fitInView()

    def fitInView(self):
        rect = QRectF(self.pixmap_item.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
            self.scale(factor, factor)

    def wheelEvent(self, event):
        factor = 1.15
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

class MainWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        
        self.viewer = ImageViewer(image_path)
        self.setCentralWidget(self.viewer)
        
        self.settings = QSettings("MyCompany", "ImageViewerApp")
        self.restoreGeometry(self.settings.value("geometry", b""))
        self.restoreState(self.settings.value("windowState", b""))

        self.resize(800, 600)

        # İkon ayarlama
        self.setWindowIcon(QIcon('icon.png'))  # İkon dosyanızın yolu

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if len(sys.argv) < 2:
        QMessageBox.critical(None, "Error", "Usage: python image.py <image-path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        viewer = MainWindow(image_path)
        viewer.show()
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        sys.exit(1)

    sys.exit(app.exec_())
