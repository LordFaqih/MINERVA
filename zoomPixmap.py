import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, pixmap):
        super().__init__()
        
        # Mengatur scene dan item
        self.scene = QGraphicsScene()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        
        # Menampilkan scene di view
        self.setScene(self.scene)
        
        # Mengatur skala awal
        self.scale_factor = 1.0
        
        # Mengatur mode tampilan
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        # Mengatur interaksi zoom
        self.setInteractive(True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        # Zoom dengan scroll
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            # Zoom in
            self.scale(zoom_in_factor, zoom_in_factor)
            self.scale_factor *= zoom_in_factor
        else:
            # Zoom out
            self.scale(zoom_out_factor, zoom_out_factor)
            self.scale_factor *= zoom_out_factor
            
    def mousePressEvent(self, event):
        # Mengatur tampilan dengan klik dan drag
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        # Mengatur tampilan dengan klik dan drag
        self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Mengatur gambar yang akan ditampilkan
    pixmap = QPixmap("images-removebg-preview.png")
    
    # Membuat objek view dan menampilkan gambar
    view = ZoomableGraphicsView(pixmap)
    view.show()
    
    sys.exit(app.exec_())
