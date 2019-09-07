from PySide2 import QtCore, QtGui, QtWidgets
# i think it would be cool to allow to build rig graphs standalone outside dcc

class TitleText(QtWidgets.QGraphicsTextItem):
    """Some usefull comment"""
    def __init__(self, text, parent=None):
        super(TitleText, self).__init__(text, parent)
    
    def sceneEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in [QtCore.Qt.Key_Space, QtCore.Qt.Key_Tab]:
                return True
            if event.key() == QtCore.Qt.Key_Return:
                self.clearFocus()
                return True
        if event.type() == QtCore.QEvent.FocusOut:
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            print "lost focus!"
            #TO DO: emit signal to update node name.
            
        return super(TitleText, self).sceneEvent(event)
        
    

class Node(QtWidgets.QGraphicsWidget ):
    """Node for representing data/operation."""
    def __init__(self, rect, pen, parent=None):
        super(Node, self).__init__(parent)
        
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        
        self.setAcceptHoverEvents(True)
        
        main_layout = QtWidgets.QGraphicsGridLayout()
        main_layout.setRowMinimumHeight(1,100)
        main_layout.setColumnMinimumWidth(0,100)
        
        self.title0 = TitleText("node", self)
        #self.title0.setText("node")
        self.title0.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.title0.setDefaultTextColor(QtCore.Qt.white)
        self.title0.setPos(QtCore.QPointF(5,0));
        #title0.setFont(QtGui.QFont("Times",10,QtGui.QFont.ExtraExpanded|QtGui.QFont.ExtraBold))
        title= QtWidgets.QGraphicsWidget(self.title0)
        main_layout.addItem(title, 0, 0)
        
        
        self.setLayout(main_layout)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        
        
        self.brush = QtGui.QBrush(QtGui.QColor("#6a717a"))
        self.setToolTip('test')
        self.parent = parent
        
        self.pen = pen
        pw = self.pen.widthF()
        
        offset = 20
        self.rect = QtCore.QRectF(rect[0], rect[1] + offset, rect[2], rect[3])
        #self.focusrect = QtCore.QRectF(rect[0]-pw/2, rect[1]-pw/2 + offset,
        #        rect[2]+pw, rect[3]+pw)
        
    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRoundedRect(self.rect, 7,7)
        self.title0.setDefaultTextColor(QtCore.Qt.white)
        if self.isSelected():
            self.drawFocusRect(painter)
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        
    def boundingRect(self):
        # bounding box rect shall be set to the bounds of the item. Due to the
        # line thickness this rect is bigger than the rect of the ellipse or rect, etc.
        return self.rect
        
    def drawFocusRect(self, painter):
        #self.focusbrush = QtGui.QBrush(QtCore.Qt.green)
        self.focuspen = QtGui.QPen()
        self.focuspen.setColor(QtGui.QColor("#83e69f"))
        self.focuspen.setWidthF(self.pen.widthF())
        #painter.setBrush(self.focusbrush)
        
        painter.setPen(self.focuspen)
        painter.drawRoundedRect(self.rect, 7,7)
        self.title0.setDefaultTextColor(QtGui.QColor("#83e69f"))
        #painter.drawRect(self.focusrect)

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(QtCore.QRectF(0, 0, 700, 700), parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None
        self.addNode()
        
    def addNode(self):
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor("black")
        pen.setWidth(1)
        self._custom_node_item = Node([0,0,100,100], pen)
        self.addItem(self._custom_node_item)
        


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        scene = GraphicsScene(self)
        view = QtWidgets.QGraphicsView(scene)
        self.setCentralWidget(view)


if __name__ == '__main__':
    import sys
    w = MainWindow()
    w.resize(750, 750)
    w.show()