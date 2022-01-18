#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/video/video.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/video/tracking.hpp>
#include "opencv2/core/cuda.hpp"
#include "opencv2/video/background_segm.hpp"
#include "opencv2/imgcodecs.hpp"


#include <rcdraw.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#include <QCoreApplication>

#include "ui_mainwindow.h"

using namespace cv;
using namespace std;


#include <iostream>


namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    int fila1,fila2;
    int umbral;



    Ui::MainWindow *ui;
    QTimer timer; // timer para el slot
    VideoCapture *cap; // objeto para la captura de un frame de video

    RCDraw *marco_original;
    RCDraw *marco_gris;
    RCDraw *marco_contraste;
    RCDraw *marco_diferencia;
    RCDraw *marco_diferencia_umbral;
    RCDraw *marco_diferencia_centroide;


    QImage *imagen_original;
    QImage *imagen_original_pintada;
    QImage *imagen_gris;
    QImage *imagen_contraste;
    QImage *imagen_diferencia;


    Mat imagen_contraste_mat, imagen_original_mat, imagen_gris_mat, imagen_diferencia_mat;


public slots:
        void compute();
};

#endif // MAINWINDOW_H
