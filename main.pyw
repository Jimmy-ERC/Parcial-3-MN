from PySide6.QtWidgets import *
from formulario import *    
from PySide6 import *
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
class MetodosNumericos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnCalcularDerivadas.clicked.connect(self.calcular)
        self.center()
    
    #Esta función centra el form en la pantalla
    def center(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        size = self.geometry()
        
        x = (screen_rect.width() - size.width()) / 2
        y = (screen_rect.height() - size.height()) / 2
        
        self.move(x, y)
    
    def advertencia(self, msg):
        dialogo = QMessageBox()
        dialogo.setIcon(QMessageBox.Warning)
        dialogo.setWindowTitle("Advertencia")
        dialogo.setText(msg)
        dialogo.setStandardButtons(QMessageBox.Ok)
        dialogo.exec()
    
    def validar_float(self,valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    def validar_funcion(self,funcion):
        try:  
            x = 1
            eval(funcion, {"x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "e": math.e, "pi": math.pi, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asin": math.asin, "asinh": math.asinh, "acos": math.acos, "acosh": math.acosh, "atan": math.atan, "atanh": math.atanh}) 
            return True
        except (SyntaxError, NameError, TypeError, ValueError):
            return False
    
    def calcular(self):
        funcion = self.ui.txtFuncion.text()
        h_text = self.ui.txtH.text()
        x_text = self.ui.txtX.text()
        xi = []
        fxi = []
        
        if funcion == "" or h_text == "" or x_text == "":
            self.advertencia("Complete todos los campos correctamente")
        elif not self.validar_float(h_text) or not self.validar_float(x_text):
            self.advertencia("Ingrese h y x correctamente")
        elif float(h_text) == 0:
            self.advertencia("h no puede ser 0")
        elif not self.validar_funcion(funcion):
            self.advertencia("Escriba correctamente la funcion")
        else:
            h = float(h_text)
            x = float(x_text)
            for i in range(11):
                xi.append([0])
                fxi.append([0])
            
            for i in range(-5, 6):
                xi[i + 5] = round(x + i * h, 4)
            
            for i in range(11):
                try:
                    fxi[i] = round(eval(funcion, {"x": xi[i], "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "e": math.e, "pi": math.pi, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asin": math.asin, "asinh": math.asinh, "acos": math.acos, "acosh": math.acosh, "atan": math.atan, "atanh": math.atanh}), 4) 
                except ValueError:
                    self.advertencia("Tenga en cuenta el dominio de la función que ha ingresado")
                    break
            
            self.ui.tableWidget.setColumnCount(2)
            self.ui.tableWidget.setHorizontalHeaderLabels(["Xi", "Fxi"])
            self.ui.tableWidget.setRowCount(11)
            
            for i in range(11):
                self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(xi[i])))
                self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(fxi[i])))
            
            self.primeraDerivada(fxi, h)
            self.segundaDerivada(fxi, h)
            self.terceraDerivada(fxi, h)
            self.cuartaDerivada(fxi, h)
    
    def primeraDerivada(self, fxi, h):
        pdAdelante = round((-(fxi[7]) + 4*(fxi[6]) -3*(fxi[5])) / (2 * h), 4)
        self.ui.lblPrimeraDerivadaAdelante.setText(str(pdAdelante))
        
        pdCentro = round((-(fxi[7]) + 8*(fxi[6]) - 8*(fxi[4]) + fxi[3]) / (12 * h), 4)
        self.ui.lblPrimeraDerivadaCentro.setText(str(pdCentro))
        
        pdAtras = round((3*(fxi[5]) - 4*(fxi[4]) + fxi[3]) / (2 * h), 4)
        self.ui.lblPrimeraDerivadaAtras.setText(str(pdAtras))
    
    def segundaDerivada(self, fxi, h):
        sdAdelante = round((-(fxi[8]) + 4*(fxi[7]) -5*(fxi[6]) + 2*(fxi[5])) / (h**2), 4)
        self.ui.lblSegundaDerivadaAdelante.setText(str(sdAdelante))
        
        sdCentro = round((-(fxi[7]) + 16*(fxi[6]) - 30*(fxi[5]) + 16*(fxi[4]) - fxi[3]) / (12*h**2), 4)
        self.ui.lblSegundaDerivadaCentro.setText(str(sdCentro))
        
        sdAtras = round((2*(fxi[5]) - 5*(fxi[4]) + 4*(fxi[3]) - (fxi[2])) / (h**2), 4)
        self.ui.lblSegundaDerivadaAtras .setText(str(sdAtras))
    
    def terceraDerivada(self, fxi, h):
        tdAdelante = round((-3*(fxi[9]) + 14*(fxi[8]) -24*(fxi[7]) + 18*(fxi[6]) - 5*(fxi[5])) / (2*h**3), 4)
        self.ui.lblTerceraDerivadaAdelante.setText(str(tdAdelante))
        
        tdCentro = round((-(fxi[8]) + 8*(fxi[7]) - 13*(fxi[6]) + 13*(fxi[4]) - 8*(fxi[3]) + fxi[2]) / (8*h**3), 4)
        self.ui.lblTerceraDerivadaCentro.setText(str(tdCentro))
        
        tdAtras = round((5*(fxi[5]) - 18*(fxi[4]) + 24*(fxi[3]) - 14*(fxi[2]) + 3*(fxi[1])) / (2*h**3), 4)
        self.ui.lblTerceraDerivadaAtras .setText(str(tdAtras))
    
    def cuartaDerivada(self, fxi, h):
        cdAdelante = round((-2*(fxi[10]) + 11*(fxi[9]) -24*(fxi[8]) + 26*(fxi[7]) - 14*(fxi[6]) + 3*(fxi[5])) / (h**4), 4)
        self.ui.lblCuartaDerivadaAdelante.setText(str(cdAdelante))
        
        cdCentro = round((-(fxi[8]) + 12*(fxi[7]) + 39*(fxi[6]) + 56*(fxi[5]) - 39*(fxi[4]) + 12*(fxi[3]) + fxi[2]) / (6*h**4), 4)
        self.ui.lblCuartaDerivadaCentro.setText(str(cdCentro))
        
        cdAtras = round((3*(fxi[5]) - 14*(fxi[4]) + 26*(fxi[3]) - 24*(fxi[2]) + 11*(fxi[1]) - 2*(fxi[0])) / (h**4), 4)
        self.ui.lblCuartaDerivadaAtras .setText(str(cdAtras))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MetodosNumericos() 
    myapp.show()
    sys.exit(app.exec())