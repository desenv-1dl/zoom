# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import psycopg2, sys, os, csv, resources, qgis.utils 
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils

class checkFeicao:  
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.AllIds=None
        self.AllLayers={}
    
    def initGui(self):    
        self.Index=None
        mc = self.canvas
        layer = mc.currentLayer()
        self.action1 = QAction(QIcon(":/plugins/zoom/back.png"), u"voltar", self.iface.mainWindow())
        self.action1.setEnabled(True)    
        self.action2 = QAction(QIcon(":/plugins/zoom/next.png"), u"próximo", self.iface.mainWindow())
        self.action2.setEnabled(True)
        self.padrao=2000
        self.action3=QLineEdit()
        self.action3.setText(str(self.padrao))    
        self.action3.textEdited.connect(self.setEscala)
        self.action3.setEnabled(True)
        self.action5=QLabel()
        self.action5.setText(u"<pre> ID: </pre>")
        self.action5.setEnabled(True)	
        self.action4=QLabel()
        self.action4.setEnabled(True)
        self.action6=QLineEdit()
        self.action6.setEnabled(True)
        QObject.connect(self.action2, SIGNAL("triggered()"), self.next)
        QObject.connect(self.action1, SIGNAL("triggered()"), self.back)
        self.action6.returnPressed.connect(self.setId) 
        self.iface.digitizeToolBar().addAction(self.action1)
        self.iface.digitizeToolBar().addAction(self.action2)
        self.iface.digitizeToolBar().addWidget(self.action3)
        self.iface.digitizeToolBar().addWidget(self.action5)
        self.iface.digitizeToolBar().addWidget(self.action4)
        self.iface.digitizeToolBar().addWidget(self.action6)
        
    def setId(self):
	try:
	    self.AllIds = sorted(self.iface.activeLayer().allFeatureIds())
        except:
            self.action6.setText("")
	    QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Não há feições ativas:<br></font><font color=blue>Adicione Feições e tente novamente!</font>", QMessageBox.Close)
	    return 1
        if int(self.action6.text()) in self.AllIds :
    	    print self.action6.text()
    	    self.Index = self.AllIds.index(int(self.action6.text()))
    	    self.action6.setText("")
    	    self.AllLayers[self.iface.activeLayer().name()]=self.Index
    	    self.action4.setText(str(self.AllIds[self.Index]))
            self.removeSelecoes()
            self.iface.activeLayer().select(self.AllIds[self.Index])        
            self.zoom()
    	else:
    	    self.action6.setText("")
    	    QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>ID inválido:<br></font><font color=blue>Entre com um ID válido!</font>", QMessageBox.Close)	
            
    def setEscala(self, texto):
        self.padrao=texto    
    
    def unload(self):    
        self.iface.digitizeToolBar().removeAction(self.action1)
        self.iface.digitizeToolBar().removeAction(self.action2)    
    
    def toggle(self):    
        mc = self.canvas
        layer = mc.currentLayer()
        if layer <> None:
            if layer.isEditable() and (layer.geometryType() == 0 or layer.geometryType() == 1 or layer.geometryType() == 2):
                self.action4.setText(u"")
                if not self.iface.activeLayer().name() in self.AllLayers.keys():		
                    self.AllLayers[self.iface.activeLayer().name()]=self.Index    
                    self.AllIds = sorted(self.iface.activeLayer().allFeatureIds())
                if self.AllLayers.get(self.iface.activeLayer().name()) !=  None:
                    self.action4.setText(str(self.AllIds[self.AllLayers.get(self.iface.activeLayer().name())]))
                elif self.AllLayers.get(self.iface.activeLayer().name()) ==  None:
                    self.action4.setText(u"")
               
    def deactivate(self):   
        self.action1.setChecked(False)
        self.action2.setChecked(False)    
    
    def next(self):
        self.AllIds = sorted(self.iface.activeLayer().allFeatureIds())
        if self.AllIds !=[]:
            self.Index=self.AllLayers.get(self.iface.activeLayer().name())
            if self.Index == None:
                self.Index = 0
                self.AllLayers[self.iface.activeLayer().name()]=self.Index    
            elif self.Index >= (len(self.AllIds)-1):
                self.Index=0
                self.AllLayers[self.iface.activeLayer().name()]=self.Index
            else:
                self.Index+=1
                self.AllLayers[self.iface.activeLayer().name()]=self.Index
            self.action4.setText(str(self.AllIds[self.Index]))
            self.removeSelecoes()
            self.iface.activeLayer().select(self.AllIds[self.Index])        
            self.zoom()
        else:
            QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Não há feições na Classe atual:<br></font><font color=blue>Adicione Feições e tente novamente!</font>", QMessageBox.Close)
            self.toggle()
    
    def back(self):
        self.AllIds = sorted(self.iface.activeLayer().allFeatureIds())
        if self.AllIds !=[]:
            self.Index=self.AllLayers.get(self.iface.activeLayer().name())
            if self.Index == None:
                self.Index = (len(self.AllIds)-1)
                self.AllLayers[self.iface.activeLayer().name()]=self.Index
            elif self.Index <= 0:
                self.Index=(len(self.AllIds)-1)
                self.AllLayers[self.iface.activeLayer().name()]=self.Index
            else:
                self.Index-=1
                self.AllLayers[self.iface.activeLayer().name()]=self.Index
            self.action4.setText(str(self.AllIds[self.Index]))
            self.removeSelecoes()    
            self.iface.activeLayer().select(self.AllIds[self.Index])
            self.zoom()    
        else:
            QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Não há feições na Classe atual:<br></font><font color=blue>Adicione Feições e tente novamente!</font>", QMessageBox.Close)
            self.toggle()    
        
    def removeSelecoes(self):
        for i in range(len(self.iface.mapCanvas().layers())):
            try:
                self.iface.mapCanvas().layers()[i].removeSelection()
            except:
                pass	
    
    def zoom(self):
        self.iface.actionZoomToSelected().trigger()
        if self.iface.activeLayer().geometryType() == 0 :
            self.iface.mapCanvas().zoomScale(float(self.padrao))




