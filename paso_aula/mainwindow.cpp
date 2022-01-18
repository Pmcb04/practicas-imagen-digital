/*La implementación de la clase Mainwindow:
   ->Constructor:
   Dibujo de la ventana principal
   Iniciar la cámara
   Crear el objeto imagen fuente  (s_img)
   Crear el objeto visor de la imagen fuente 1 (visor_source)
    Arrancar el connect para el compute
   ->Destructor:
   ->compute (en SLOT) :
   Declarar las matrices imagen Mat:

   Capturar un frame de una cámara

   Procesar la imagen de una cámara


   Actualizar los visores.
*/
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <qdebug.h>
#include <iostream>   // std::cout


vector<vector<Point> > contours;
vector<Vec4i> hierarchy;

using namespace std;
// Constructor member
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    cap= new VideoCapture();
    cap->open("video.wmv");

    cap->set(CV_CAP_PROP_FRAME_WIDTH,320); // fix width
    cap->set(CV_CAP_PROP_FRAME_HEIGHT,240); // fix heigth


    fila1=125;
    fila2=200;

    umbral=90;


    // se encuentra dentro de la sala al empezar la simulación


    this->imagen_original = new QImage(320,240, QImage::Format_RGB888);
    this->imagen_gris = new QImage(320,240, QImage::Format_Indexed8);
    this->imagen_contraste = new QImage(320,240, QImage::Format_Indexed8);
    this->imagen_diferencia = new QImage(320,240, QImage::Format_Indexed8);





    marco_original = new RCDraw(320,240, imagen_original, ui->marco_original);
    marco_gris = new RCDraw(320,240, imagen_gris, ui->marco_gris);
    marco_contraste = new RCDraw(320,240, imagen_contraste, ui->marco_contraste);
    marco_diferencia = new RCDraw(320,240, imagen_diferencia, ui->marco_diferencia);


    //Cargamos la primera imagen como imagen de contraste para realizar la resta:
    cap->read(imagen_contraste_mat);
    //Adaptamos al tamaño y pasamos a gris
    cv::resize(imagen_contraste_mat, imagen_contraste_mat,Size(320,240));
    cvtColor(imagen_contraste_mat, imagen_contraste_mat, CV_RGB2GRAY);
    //Mostramos por pantalla
    memcpy(imagen_contraste->bits(),imagen_contraste_mat.data, imagen_contraste_mat.rows*imagen_contraste_mat.cols);
    marco_contraste->update();

    connect(&timer,SIGNAL(timeout()),this,SLOT(compute()));
    timer.start(100);


}

// Destructor member
MainWindow::~MainWindow()
{
    delete ui;
    delete cap;
    delete imagen_original;
    delete imagen_gris;
    delete imagen_contraste;
    delete imagen_diferencia;
    delete marco_original;
    delete marco_gris;
    delete marco_contraste;
    delete marco_diferencia;
    delete marco_diferencia_umbral;
    delete marco_diferencia_centroide;

 }





// implementación del bucle de proceso en SLOT
void MainWindow::compute()
{
   ////////////////// CAMERA  //////////////////////////
   if(!cap->isOpened())  // check if we succeeded
       exit(-1);
   // Cogemos la imagen de la camara
   *cap >> imagen_original_mat;

   // BGR to RGB   Pasamos la imagen a RGB
   cvtColor(imagen_original_mat, imagen_original_mat, CV_BGR2RGB,1);
    Mat temp;


   //Pintamos las lineas de barrera en la entrada
   imagen_original_mat.copyTo(temp);

   cv::line(temp,Point(0,fila1),Point(temp.cols-1,fila1),CV_RGB(0,0,255),1);
   cv::line(temp,Point(0,fila2),Point(temp.cols-1,fila2),CV_RGB(0,0,255),1);


   memcpy(imagen_original->bits(),temp.data, temp.rows*temp.cols*sizeof(uchar)*3 );
   marco_original->update();

   // RGB2GRAY  Pasamos a gris la imagen
   cvtColor(imagen_original_mat, imagen_gris_mat, CV_RGB2GRAY,1);

   // Pintamos por el visor de gris
   memcpy(imagen_gris->bits(), imagen_gris_mat.data, imagen_gris_mat.rows*imagen_gris_mat.cols*sizeof(uchar));
   this->marco_gris->update();
   // Calculamos la diferencia entre ambas imagenes
   absdiff(imagen_gris_mat,imagen_contraste_mat, imagen_diferencia_mat);

   memcpy(imagen_diferencia->bits(),imagen_diferencia_mat.data, imagen_diferencia_mat.rows*imagen_diferencia_mat.cols*sizeof(uchar));
   marco_diferencia->update();
}


