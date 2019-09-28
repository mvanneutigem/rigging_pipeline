from PySide2 import QtCore, QtGui, QtWidgets
# i think it would be cool to allow to build rig graphs standalone outside dcc


class Path(QtWidgets.QGraphicsPathItem):
    def __init__(self, path, scene):
        super(Path, self).__init__(path)
        self.width = 1
        self.setPen(QtGui.QPen(QtCore.Qt.white, self.width))        

    def updateElement(self, index, pos):
        path = self.path()
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)
    
    def shape(self):
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(self.width)
        qp.setCapStyle(Qt.SquareCap)
        return qp.createStroke(self.path())

class AttributeWidget(QtWidgets.QGraphicsWidget):
    """Input connection display for attributes"""
    def __init__(self, name, has_output=True, has_input=True, rect=QtCore.QRectF(0,0,100,20), index=0, parent=None):
        print parent
        super(AttributeWidget, self).__init__( parent)
        
        main_layout = QtWidgets.QGraphicsGridLayout()
        self.title0 = QtWidgets.QGraphicsTextItem(name, self)
        self.title0.setDefaultTextColor(QtCore.Qt.black)
        self.title0.setPos(QtCore.QPointF(7.5,rect.top()));
        title = QtWidgets.QGraphicsWidget(self.title0)
        main_layout.addItem(title, 0, 0)
        self.setLayout(main_layout)
        
        self.has_output = has_output
        self.has_input = has_input
        
        
        self.output_connection = None
        self.input_connection = None
        
        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setColor("black")
        self.pen.setWidth(1)
        self.brush = QtGui.QBrush(QtGui.QColor("white"))
        
        if index%2:
            self.background_brush = QtGui.QBrush(QtGui.QColor("#426969"))
        else:
            self.background_brush = QtGui.QBrush(QtGui.QColor("#548787"))
        
        self.rect = rect
        print self.rect
        self.setGeometry(self.rect)
        
    def boundingRect(self):
        return self.rect
        
    def setGeometry(self, rect):
        self.prepareGeometryChange()
        super(AttributeWidget, self).setGeometry(rect)
        radius = 5
        self.input_shape = QtCore.QRectF(
            self.rect.left(), 
            radius + rect.top(),
            2*radius, 
            2*radius
        )
        self.output_shape = QtCore.QRectF(
            self.rect.right() -  2* radius,
            radius + rect.top(),
            2*radius,
            2*radius
        )
        
    def paint(self, painter, option, widget):
        painter.setBrush(self.background_brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(
            QtCore.QRectF(self.rect.left() + 6, self.rect.top()+1, self.rect.width() -12, self.rect.height()-2), 
            7,
            7
        )
        
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        self.title0.setDefaultTextColor(QtCore.Qt.black)
        if self.has_output:
            painter.drawEllipse(self.output_shape)
        if self.has_input:
            painter.drawEllipse(self.input_shape)    
    
    def _getMidPoint(self):
        return QtCore.QPointF(
            (self.geometry().right() + self.geometry().left())/2.0 - self.geometry().left(), 
            (self.geometry().top() + self.geometry().bottom())/2.0 - self.geometry().top()
        )
        
    def addOutputConnection(self, attribute):
        #TO DO add connection here
        self.output_connection = attribute
        self.output_path = Path()
        self.output_path.updateElement(
            0, 
            self._getRectMidPosition(self.output_shape)
        )
        
        attribute.addInputConnection(self, self.output_path)
        
    def addInputConnection(self, attribute, path):
        self.input_connection = attribute
        self.input_path = path
        self.input_path.updateElement(
            1, 
            self._getRectMidPosition(self.input_shape)
        )
    
    def itemChange(self, change, value):
        super(AttributeWidget, self).itemChange(change, value)
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            if self.output_connection:
                self.output_path.updateElement(0, self._getRectMidPosition(self.output_shape))
            if self.input_connection:
                self.input_path.updateElement(1, self._getRectMidPosition(self.input_shape))
        return QtWidgets.QGraphicsWidget.itemChange(self, change, value)

class TitleText(QtWidgets.QGraphicsTextItem):
    """Some usefull comment"""
    changed = QtCore.Signal(str)
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
            #TO DO: emit signal to update node name.
            self.changed.emit(self.toPlainText())
            
        return super(TitleText, self).sceneEvent(event)
        
    

class Node(QtWidgets.QGraphicsWidget ):
    """Node for representing data/operation."""
    def __init__(self, pen, parent=None):
        super(Node, self).__init__(parent)
        
        self.name = 'node'
        self.attributes = {}
        
                
        self.rect = QtCore.QRectF(0,20,100, 40)
        #self.rect = QtCore.QRectF(rect[0], rect[1] + offset, rect[2], rect[3])
        self.setGeometry(self.rect)
        
        print "create node"
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        
        self.setAcceptHoverEvents(True)
        
        main_layout = QtWidgets.QGraphicsGridLayout()
        
        self.title0 = TitleText(self.name, self)
        self.title0.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.title0.setDefaultTextColor(QtCore.Qt.white)
        self.title0.setPos(QtCore.QPointF(5,0));
        #title0.setFont(QtGui.QFont("Times",10,QtGui.QFont.ExtraExpanded|QtGui.QFont.ExtraBold))
        title= QtWidgets.QGraphicsWidget(self.title0)
        main_layout.addItem(title, 0, 0)
        
        self.attribute_holder = QtWidgets.QGraphicsWidget()
        #attribute layout is unnecessary
        self.attribute_layout = QtWidgets.QGraphicsGridLayout()
        self.attribute_holder.setLayout(self.attribute_layout)
        
        main_layout.addItem(self.attribute_holder, 1,0)
        self.title0.changed.connect(self.setName)
        self.setLayout(main_layout)
        
        
        self.brush = QtGui.QBrush(QtGui.QColor("#548787"))
        self.setToolTip('test')
        self.parent = parent
        
        self.pen = pen
        pw = self.pen.widthF()
        
        self.setGeometry(self.rect.left(), self.rect.top(), self.rect.right(), self.rect.bottom() + 20)

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRoundedRect(self.rect, 7,7)
        self.title0.setDefaultTextColor(QtCore.Qt.white)
        if self.isSelected():
            self.drawFocusRect(painter)
            self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)        
        
        
    def boundingRect(self):
        return self.rect
        
    def drawFocusRect(self, painter):
        self.focuspen = QtGui.QPen()
        self.focuspen.setColor(QtGui.QColor("#83e69f"))
        self.focuspen.setWidthF(self.pen.widthF())
        
        painter.setPen(self.focuspen)
        painter.drawRoundedRect(self.rect, 7,7)
        self.title0.setDefaultTextColor(QtGui.QColor("#83e69f"))
        
    def update_rect(self):
        self.prepareGeometryChange()
        self.rect = QtCore.QRectF(0,20,100, 20 * len(self.attributes))
        self.setGeometry(self.rect.left(), self.rect.top(), self.rect.right(), self.rect.bottom() + 20)
        
    def setName(self, name):
        print 'set name', name
        self.name = name
        
    def addAttribute(self, name, has_input=True, has_output=True):
        print 'add attribute'
        #attribute = 
        index = len(self.attributes)
        height = 20
        width = 110
        rect = QtCore.QRectF(
            self.rect.left() -2.5,
            self.rect.top() - 10 + 10 * len(self.attributes),
            width,
            height )
        self.attributes[name] = [index,
            AttributeWidget(
                name, 
                has_input, 
                has_output,
                rect=rect,
                index=index,
                parent=self
            )
        ]
        self.update_rect()
        return self.attributes[name][1]
        
    def removeAttribute(self, name):
        print 'remove attribute'
        self.attribute_layout.removeWidget(self.attributes[name])
        self.update_rect()
        

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None
        self.addNode()
        
    def addNode(self):
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor("black")
        pen.setWidth(1)
        self._custom_node_item = Node(pen)
        self._custom_node_item.addAttribute('Tip')
        self._custom_node_item.addAttribute('End', has_input=False)
        self.addItem(self._custom_node_item)
        

class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super(GraphicsView, self).__init__(scene)
        self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        self.originX = 0
        self.originY = 0
                
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.MidButton):
            #Store original position.
            self.originX = event.x()
            self.originY = event.y()
        super(GraphicsView, self).mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.MidButton):
            oldp = self.mapToScene(self.originX, self.originY)
            newp = self.mapToScene(event.pos())
            translation = newp - oldp
    
            old_transform = QtGui.QTransform()

            scene_rect = self.scene().sceneRect()
            new_scene_rect = QtCore.QRectF(scene_rect.x()-translation.x(),
                                  scene_rect.y()-translation.y(),
                                  scene_rect.width(),scene_rect.height())
            self.scene().setSceneRect(new_scene_rect)
            
            self.setTransform(old_transform)

            self.originX = event.x()
            self.originY = event.y()
        super(GraphicsView, self).mouseMoveEvent(event)
   

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        scene = GraphicsScene(self)
        view = GraphicsView(scene)
        view.setBackgroundBrush(QtGui.QBrush(QtGui.QColor('black'), QtCore.Qt.DiagCrossPattern))
        
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(view)
        self.setLayout(main_layout)


if __name__ == '__main__':
    import sys
    w = MainWindow()
    w.resize(750, 750)
    w.show()