#include <Keypad.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(2,3,4,5,6,7);
const byte FILAS = 4;
const byte COLUMNAS = 4;


byte filaPins[FILAS]={A0, A1, A2, A3}; 
byte columnaPins[COLUMNAS]={11, 10, 9, 8};

int tmenu = 0;
int tmenu2 = 0;

int ronda = 1;///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

boolean barcosLlenos = false;
boolean tirosLlenos = false;

char tecla=' ';

int scoreA = 0;
int scoreB = 0;

int targetA=0;
int targetB=0;

int valormenubarcos=0;

int barcosA[4][10];
int barcosB[4][10];
int tirosA[4][10];
int tirosB[4][10];

int contadorbarco=0;
String mensaje= " ";
int coordenada[2];
int cont =0;
int matriz[4][10];


char hexaKeys[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

Keypad teclado = Keypad(makeKeymap(hexaKeys), filaPins, columnaPins, FILAS, COLUMNAS);

// ***********************************************************************************
// ** Notas para la melodia de victoria - Song of Storms 

    #define NOTE_B0  31
    #define NOTE_C1  33
    #define NOTE_CS1 35
    #define NOTE_D1  37
    #define NOTE_DS1 39
    #define NOTE_E1  41
    #define NOTE_F1  44
    #define NOTE_FS1 46
    #define NOTE_G1  49
    #define NOTE_GS1 52
    #define NOTE_A1  55
    #define NOTE_AS1 58
    #define NOTE_B1  62
    #define NOTE_C2  65
    #define NOTE_CS2 69
    #define NOTE_D2  73
    #define NOTE_DS2 78
    #define NOTE_E2  82
    #define NOTE_F2  87
    #define NOTE_FS2 93
    #define NOTE_G2  98
    #define NOTE_GS2 104
    #define NOTE_A2  110
    #define NOTE_AS2 117
    #define NOTE_B2  123
    #define NOTE_C3  131
    #define NOTE_CS3 139
    #define NOTE_D3  147
    #define NOTE_DS3 156
    #define NOTE_E3  165
    #define NOTE_F3  175
    #define NOTE_FS3 185
    #define NOTE_G3  196
    #define NOTE_GS3 208
    #define NOTE_A3  220
    #define NOTE_AS3 233
    #define NOTE_B3  247
    #define NOTE_C4  262
    #define NOTE_CS4 277
    #define NOTE_D4  294
    #define NOTE_DS4 311
    #define NOTE_E4  330
    #define NOTE_F4  349
    #define NOTE_FS4 370
    #define NOTE_G4  392
    #define NOTE_GS4 415
    #define NOTE_A4  440
    #define NOTE_AS4 466
    #define NOTE_B4  494
    #define NOTE_C5  523
    #define NOTE_CS5 554
    #define NOTE_D5  587
    #define NOTE_DS5 622
    #define NOTE_E5  659
    #define NOTE_F5  698
    #define NOTE_FS5 740
    #define NOTE_G5  784
    #define NOTE_GS5 831
    #define NOTE_A5  880
    #define NOTE_AS5 932
    #define NOTE_B5  988
    #define NOTE_C6  1047
    #define NOTE_CS6 1109
    #define NOTE_D6  1175
    #define NOTE_DS6 1245
    #define NOTE_E6  1319
    #define NOTE_F6  1397
    #define NOTE_FS6 1480
    #define NOTE_G6  1568
    #define NOTE_GS6 1661
    #define NOTE_A6  1760
    #define NOTE_AS6 1865
    #define NOTE_B6  1976
    #define NOTE_C7  2093
    #define NOTE_CS7 2217
    #define NOTE_D7  2349
    #define NOTE_DS7 2489
    #define NOTE_E7  2637
    #define NOTE_F7  2794
    #define NOTE_FS7 2960
    #define NOTE_G7  3136
    #define NOTE_GS7 3322
    #define NOTE_A7  3520
    #define NOTE_AS7 3729
    #define NOTE_B7  3951
    #define NOTE_C8  4186
    #define NOTE_CS8 4435
    #define NOTE_D8  4699
    #define NOTE_DS8 4978
    #define REST      0

    int tempo_W = 130;
    int tempo_L = 200;
    
    int buzzer = 12;
    
    int melody_W[] = {
      
      // Song of storms - The Legend of Zelda Ocarina of Time. 
    
      NOTE_D4,8, NOTE_F4,8, NOTE_D5,2,
      
      NOTE_D4,8, NOTE_F4,8, NOTE_D5,2,
      NOTE_E5,-4, NOTE_F5,8, NOTE_E5,8, NOTE_E5,8,
      NOTE_E5,8, NOTE_C5,8, NOTE_A4,2,
      NOTE_A4,4, NOTE_D4,4, NOTE_F4,8, NOTE_G4,8,
      NOTE_A4,-2,
      NOTE_A4,4, NOTE_D4,4, NOTE_F4,8, NOTE_G4,8,
      NOTE_E4,-2,
    
    };

// ***********************************************************************************

// ** Notas para la melodia de derrota - Game Over (Super Mario Bros)

      int melody_L[] = {
      
        // Super Mario Bros theme
        
        //game over sound
        NOTE_C5,-4, NOTE_G4,-4, NOTE_E4,4, //45
        NOTE_A4,-8, NOTE_B4,-8, NOTE_A4,-8, NOTE_GS4,-8, NOTE_AS4,-8, NOTE_GS4,-8,
        NOTE_G4,8, NOTE_D4,8, NOTE_E4,-2,  
      
      };

// ***********************************************************************************


void setup() {
  Serial.begin(115200);
  lcd.begin(16,2);
  lcd.clear();
  lcd.setCursor(0,0);
  pinMode(buzzer,OUTPUT);
}

void loop() {
  menu();
}


void melodiaVictoria () {

// sizeof da el número de bytes, cada valor int se compone de dos bytes (16 bits)
// hay dos valores por nota (tono y duración), por lo que para cada nota hay cuatro bytes
int notes = sizeof(melody_W) / sizeof(melody_W[0]) / 2;

int wholenote = (60000 * 4) / tempo_W;  // La duración completa de una nota entera

int divider = 0, noteDuration = 0;

  // Iteración una tras otra de las notas de la melodía
  // El tamaño del arreglo es el doble de la cantidad del número de notas
  
  for (int thisNote = 0; thisNote < notes * 2; thisNote = thisNote + 2) {

    divider = melody_W[thisNote + 1];  // Cálculo de la duración de cada nota
      if (divider > 0) {
        noteDuration = (wholenote) / divider;  // Nota regular
      } else if (divider < 0) {
        noteDuration = (wholenote) / abs(divider);  // Puntos - Duraciones negativas
        noteDuration *= 1.5; // Aumento de la duracion en la mitad de la nota
       }

    tone(buzzer, melody_W[thisNote], noteDuration*0.9); // Nota con duración del 90%, 10% pausa
    delay(noteDuration); // Espera a la siguiente nota especificada
    noTone(buzzer); // Espera a la generavión de la forma de onda de la siguiente nota
  }
}

void melodiaDerrota () {

  int notes = sizeof(melody_L) / sizeof(melody_L[0]) / 2;

  int wholenote = (60000 * 4) / tempo_L;
  
  int divider = 0, noteDuration = 0;


  for (int thisNote = 0; thisNote < notes * 2; thisNote = thisNote + 2) {

    divider = melody_L[thisNote + 1];
    if (divider > 0) {
      noteDuration = (wholenote) / divider;
    } else if (divider < 0) {
        noteDuration = (wholenote) / abs(divider);
        noteDuration *= 1.5; // increases the duration in half for dotted notes
    }

    tone(buzzer, melody_L[thisNote], noteDuration * 0.9);

    delay(noteDuration);

    noTone(buzzer);
  }
}

void menu(){
  while(tmenu == 0){
      lcd.setCursor(0,0);
      lcd.print("1.- Comenzar");
      lcd.setCursor(0,1);
      lcd.print("2.- Salir");   
      tecla = teclado.getKey();
      switch (tecla){
         case '1': lcd.clear();
                   delay(700);
                   tmenu = 1;
                   menuJuego();
                   break;
          case '2':exit;
                   break;
      }
  }
}



void llenarMatriz(int tipo, int tipobarco){
    int cont2p=0;
    int cont3p=0;
    int contadormisil=0;
    if (tipo==1){
      while(contadorbarco<10){
          //llenar barcos
          lcd.clear();
          lcd.print("Ingresa Coordena");
          mensaje = "da de barco: ";
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          tecla = '1';
          while(tecla != 'A'&&tecla != 'B'&&tecla != 'C'&&tecla != 'D')
          {
            tecla = teclado.getKey(); //Obtengo el primer caracter del teclado
          }
          switch(tecla){
            case 'A': coordenada[0]=0;
                  break;
            case 'B': coordenada[0]=1;
                  break;
            case 'C': coordenada[0]=2;
                  break;
            case 'D': coordenada[0]=3;
                  break;
          }
          mensaje += (String)tecla +"x";
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          tecla = 'A';
          while(tecla != '1'&&tecla != '2'&&tecla != '3'&&tecla != '4'&&tecla != '5'&&tecla != '6'&&tecla != '7'&&tecla != '8'&&tecla != '9'&&tecla != '0')
          {
            tecla = teclado.getKey(); //Obtengo el primer caracter del teclado
          }
          coordenada[1]=atoi(&tecla);
          mensaje += (String)tecla;
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          delay(700);
          if(matriz[coordenada[0]][coordenada[1]]!=1){    //Quiere decir que en esa casilla no hay un barco}
            if(tipobarco==1){
              contadorbarco++;
              matriz[coordenada[0]][coordenada[1]]=1;            
              barcosA[coordenada[0]][coordenada[1]]=1;
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print("BARCO DE 1 POSIC");
              lcd.setCursor(0,1);
              lcd.print("CION INGRESADO");
              delay(750);
              if(contadorbarco == 10){
                  lcd.clear();
                  lcd.setCursor(0,0);
                  lcd.print("SE INGRESARON");
                  lcd.setCursor(0,1);
                  lcd.print("LOS 10 BARCOS");
              }
              delay(900);
              break;
            }
            else{
              if(tipobarco==2){
                cont2p++;
                matriz[coordenada[0]][coordenada[1]]=1;            
                barcosA[coordenada[0]][coordenada[1]]=1;
                if(cont2p==2){
                  contadorbarco++;
                  lcd.clear();
                  lcd.setCursor(0,0);
                  lcd.print("BARCO DE 2 POSIC");
                  lcd.setCursor(0,1);
                  lcd.print("CIONES INGRESADO");
                  delay(750);
                  if(contadorbarco == 10){
                    lcd.clear();
                    lcd.setCursor(0,0);
                    lcd.print("SE INGRESARON");
                    lcd.setCursor(0,1);
                    lcd.print("LOS 10 BARCOS");
                  } 
                  delay(900);
                  break;
                }
              }
              else{
                   if(tipobarco==3){
                      cont3p++;
                      matriz[coordenada[0]][coordenada[1]]=1;            
                      barcosA[coordenada[0]][coordenada[1]]=1;
                      if(cont3p==3){
                        contadorbarco++;
                        lcd.clear();
                        lcd.setCursor(0,0);
                        lcd.print("BARCO DE 3 POSIC");
                        lcd.setCursor(0,1);
                        lcd.print("CIONES INGRESADO");
                        delay(750);
                        if(contadorbarco == 10){
                          lcd.clear();
                          lcd.setCursor(0,0);
                          lcd.print("SE INGRESARON");
                          lcd.setCursor(0,1);
                          lcd.print("LOS 10 BARCOS");
                        }
                        delay(900);
                         break;
                      }
                   }
               }
            }
        }//if de comprobar si esta vacia una coordenada
        else{         
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("ERROR COORDENADA");
          lcd.setCursor(0,1);
          lcd.print("YA INGRESADA");
          delay(2400);
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("INTENTE DE");
          lcd.setCursor(0,1);
          lcd.print("NUEVO");
        }
      }
    }
    else{
        while (contadormisil<10){
        //llenar misiles
          lcd.print("Ingresa Coordena");
          mensaje = "da de misil: ";
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          tecla = '1';
          while(tecla != 'A'&&tecla != 'B'&&tecla != 'C'&&tecla != 'D')
          {
          tecla = teclado.getKey(); //Obtengo el primer caracter del teclado
          }
          switch(tecla){
            case 'A': coordenada[0]=0;
                  break;
            case 'B': coordenada[0]=1;
                  break;
            case 'C': coordenada[0]=2;
                  break;
            case 'D': coordenada[0]=3;
                  break;
          }

          mensaje += (String)tecla +"x";
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          tecla = 'A';
          while(tecla != '1'&&tecla != '2'&&tecla != '3'&&tecla != '4'&&tecla != '5'&&tecla != '6'&&tecla != '7'&&tecla != '8'&&tecla != '9'&&tecla != '0')
          {
            tecla = teclado.getKey(); //Obtengo el primer caracter del teclado
          }

          coordenada[1]=atoi(&tecla);
          mensaje += (String)tecla;
          lcd.setCursor(0,1);
          lcd.print(mensaje);
          if(matriz[coordenada[0]][coordenada[1]]!=1){//Quiere decir que en esa casilla no hay un misil
              contadormisil++;
              matriz[coordenada[0]][coordenada[1]]=1;
              tirosA[coordenada[0]][coordenada[1]]=1;
          }else{  
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("ERROR COORDENADA");
          lcd.setCursor(0,1);
          lcd.print("YA INGRESADA");
          delay(2400);
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("INTENTE DE");
          lcd.setCursor(0,1);
          lcd.print("NUEVO");
        }
        if (contadormisil == 10){
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("SE INGRESARON");
          lcd.setCursor(0,1);
          lcd.print("LOS 10 MISILES");
        }
        delay(900);
        lcd.clear();          
      }
    }
}

void menuBarcos(){
   lcd.setCursor(0,0);
   lcd.print("TAMANIOS DE LOS");
   lcd.setCursor(0,1);
   lcd.print("BARCOS");
   delay(1700);
   lcd.clear();
   while (tmenu2 == 0){
       lcd.setCursor(0,0);
       lcd.print("A)3 B)2 C)1");
       lcd.setCursor(0,1);
       lcd.print("BARCOS DISP: "+String(10 - contadorbarco));
       tecla = teclado.getKey();
       if(tecla == 'A'){
          valormenubarcos=3;
          tmenu2 = 1;
       }
       else{
           if(tecla == 'B'){
              valormenubarcos=2;
              tmenu2 = 1;
           }
           else{
               if(tecla == 'C'){
                  valormenubarcos=1;
                  tmenu2 = 1;
               }
           }
       }
   }
}


void menuJuego(){
 while(tmenu > 0){
      while(tmenu == 1){
        lcd.setCursor(0,0);
        lcd.print("1.IngresarBarcos");
        lcd.setCursor(0,1);
        lcd.print("2.Disparar C.Mas");
        tecla = teclado.getKey();
        switch (tecla){
            case '1':lcd.clear();
                    delay(900);
                    limpiarMatriz();
                    limpiarMatrizJA(1);
                    while(contadorbarco<10){
                      menuBarcos();
                      lcd.clear();
                      llenarMatriz(1,valormenubarcos);
                      lcd.clear();
                      tmenu2 = 0;
                    }
                    contadorbarco = 0;
                    barcosLlenos = true;
                    break;     

           case '2': lcd.clear();
                     delay(500);
                     limpiarMatriz();
                     limpiarMatrizJA(0);
                     llenarMatriz(0,0);
                     tirosLlenos = true; 
                     break;

           case 'C': lcd.clear();
                     delay (500);
                     tmenu = 2;
                     break;
        } // Cierre del switch case 
        
      } // Cierre del tmenu = 1

    while(tmenu==2){
      lcd.setCursor(0,0);
      lcd.print("3.Ver Barcos");
      lcd.setCursor(0,1);
      lcd.print("B.Volver   C.Mas");
      tecla = teclado.getKey();
      switch (tecla){
        case 'B': lcd.clear();
                  tmenu=1;
                  break;
                  
        case '3': lcd.clear();;
                  delay(500);
                  imprimirBarcosA();
                  break;
                  
        case 'C': lcd.clear();;
                  delay(500);
                  tmenu=3;
                  break;
      }
    }

     while(tmenu==3){
      
      lcd.setCursor(0,0);
      lcd.print("4.Ver Disparos");
      lcd.setCursor(0,1);
      lcd.print("B.Volver   C.Mas");
      tecla = teclado.getKey();
      switch (tecla){
        case 'B':lcd.clear();
              tmenu=2;
              break;
        case '4': lcd.clear();
                  delay(500);
                  imprimirTirosA();
              break;
        case 'C': lcd.clear();
                  delay(500);
                  tmenu=4;
              break;
      }
    }

    while(tmenu==4){
     
      lcd.setCursor(0,0);
      lcd.print("5.Jugar");
      lcd.setCursor(0,1);
      lcd.print("B.Volver   C.Mas");
      tecla = teclado.getKey();
      switch (tecla){
        case '5':lcd.clear();
              delay(500);
              jugar();
              break;
        case 'B': lcd.clear();
              delay(500);
              tmenu=3;
              break;
        case 'C': lcd.clear();
                delay(500);
                tmenu=5;
                break;
      }
    }

    while(tmenu==5){
      lcd.setCursor(0,0);
      lcd.print("6.Ver puntaje");
      lcd.setCursor(0,1);
      lcd.print("B.Volver   C.Mas");
      tecla = teclado.getKey();
      switch (tecla){
        case '6':lcd.clear();
              delay(500);
              
              break;
        case 'B': lcd.clear();;
              delay(500);
              tmenu=4;
              break;
        case 'C': lcd.clear();;
              delay(500);
              tmenu=6;
              break;
      }
    }

    while(tmenu==6){
      lcd.setCursor(0,0);
      lcd.print("7.Salir");
      lcd.setCursor(0,1);
      lcd.print("B.Volver");
      tecla = teclado.getKey();
      switch (tecla){
        case '7':lcd.clear();
                 delay(500);
                 tmenu=0;
                 break;
        case 'B': lcd.clear();
              delay(500);
              tmenu=5;
              break;
      }
    } 

    if(scoreA==2){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("HAS GANADO");
      lcd.setCursor(0,1);
      lcd.print("FELICIDADES");
      delay(2600);
    }
    if(scoreB==2){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("F HAS PERDIDO :(");
      lcd.setCursor(0,1);
      lcd.print("SUERTE LA PROX");
      delay(2600);
    }
      
 } // while (tmenu > 0) 
} // Menu juego 


void imprimirBarcosA(){
  
  int cont=0;
  int fila = 0;
  while(fila<4){
      cont = 0;
      lcd.setCursor(0,1); //Algoritmo para llenar la fila de abajo del lcd
      lcd.print('[');
      while(cont<10){ //Algoritmo para imprimir las filas de abajo
        if (barcosA[fila][cont]==1){
          lcd.setCursor(cont+1,1);
          lcd.print('O');
        }else{
          lcd.setCursor(cont+1,1);
          lcd.print('-');
        }
        cont++;
      }
      lcd.setCursor(11,1);
      lcd.print(']');
      cont=0;
      if (fila != 0){
          lcd.setCursor(0,0); //Algoritmo para llenar la fila de arriba del lcd
          lcd.print('[');
          while(cont<10){ //Algoritmo para imprimir las filas de abajo
            if (barcosA[fila-1][cont]==1){
              lcd.setCursor(cont+1,0);
              lcd.print('O');
            }else{
              lcd.setCursor(cont+1,0);
              lcd.print('-');
            }
            cont++;
          }
          lcd.setCursor(11,0);
          lcd.print(']');
      }
          
      delay(2000);
      fila++;
    lcd.clear();
  }
}//fin de imprimirbarcos

void imprimirTirosA(){
  
  int cont=0;
  int fila = 0;
  while(fila<4){
      cont = 0;
      lcd.setCursor(0,1); //Algoritmo para llenar la fila de abajo del lcd
      lcd.print('[');
      while(cont<10){ //Algoritmo para imprimir las filas de abajo
        if (tirosA[fila][cont]==1){
          lcd.setCursor(cont+1,1);
          lcd.print('X');
        }else{
          lcd.setCursor(cont+1,1);
          lcd.print('-');
        }
        cont++;
      }
      lcd.setCursor(11,1);
      lcd.print(']');
      cont=0;
      if (fila != 0){
          lcd.setCursor(0,0); //Algoritmo para llenar la fila de arriba del lcd
          lcd.print('[');
          while(cont<10){ //Algoritmo para imprimir las filas de abajo
            if (tirosA[fila-1][cont]==1){
              lcd.setCursor(cont+1,0);
              lcd.print('X');
            }else{
              lcd.setCursor(cont+1,0);
              lcd.print('-');
            }
            cont++;
          }
          lcd.setCursor(11,0);
          lcd.print(']');
      }
          
      delay(2000);
      fila++;
    lcd.clear();
  }
}//fin de imprimirtiros


void limpiarMatriz(){
  for(int i=0; i<=3; i++){//Limpio la matriz temporal, todas las casillas en 0
        for(int j=0; j<=9; j++){
          matriz[i][j]=0;
        } 
    }
}

void limpiarMatrizJA(int tipo){
  if(tipo==1){
    for(int i=0; i<=3; i++){
      for(int j=0; j<=9; j++){
        barcosA[i][j]=0;
      } 
    }
  }else{
    for(int i=0; i<=3; i++){
      for(int j=0; j<=9; j++){
        tirosA[i][j]=0;
      }
    } 
  }
}//fin de limpiarmatriz

void jugar(){
  
  
  if(!barcosLlenos||!tirosLlenos){
    digitalWrite(11, HIGH);
              delay(700);
              digitalWrite(11, LOW);
              digitalWrite(11, HIGH);
              delay(700);
              digitalWrite(11, LOW);
    lcd.setCursor(0,0);
    lcd.print("Asegurate de");
    lcd.setCursor(0,1);
    lcd.print("llenar todas");
    delay(2500);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("las matrices");
    delay(2500);
    lcd.clear();
  }else{
    lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Recibiendo datos");
  lcd.setCursor(0,1);
  lcd.print("de Jugador B");
    digitalWrite(11, HIGH);
              delay(700);
              digitalWrite(11, LOW);
              digitalWrite(11, HIGH);
              delay(700);
              digitalWrite(11, LOW);
              digitalWrite(11, HIGH);
              delay(700);
              digitalWrite(11, LOW);
    int x=0;
    int y=0;
    int cont=0;
    bool condicion= true;
    
    char letra = ' ';
    while (condicion == true ){ //Ciclo para recibir los barcos de Python
      letra = Serial.read();
      if (letra=='1'||letra=='2'||letra=='3'||letra=='4'||letra=='5'||letra=='6'||letra=='7'||letra=='8'||letra=='9'||letra=='0'){
        if (cont==0){
          x=atoi(&letra);
          cont++;
        }else{ //Ya recibi la segunda coordenada, puedo aumentar el contador de coordenadas recibidas
          y=atoi(&letra);
          cont++;
        }
        if(cont==2){
          cont=0;
          barcosB[x][y]=1;
          if(barcosB[x][y]==tirosA[x][y]){ //Signiica que yo le di al jugador de python
            targetA++; 
          }
        }
      }
      else{
          if(letra == 'P' ){
            condicion = false; 
          }
      }
    }
    int cant = 0;
    cont = 0;
    letra = ' ';
    while (cant<10){ //Ciclo para recibir los disparos de python
      letra = Serial.read();
      if (letra=='1'||letra=='2'||letra=='3'||letra=='4'||letra=='5'||letra=='6'||letra=='7'||letra=='8'||letra=='9'||letra=='0'){
        if (cont==0){
          x=atoi(&letra);
          cont++;
        }else{ //Ya recibi la segunda coordenada, puedo aumentar el contador de coordenadas recibidas
          y=atoi(&letra);
          cont++;
          cant++;
        }
        if(cont==2){
          cont=0;
          tirosB[x][y]=1;
          if(tirosB[x][y]==barcosA[x][y]){ //Signiica que el jugador python me dio a mi
            targetB++; 
          }
        }
      }//fin del read
    }
    if(ronda == 1){
    if (Serial.availableForWrite() > 0){
      lcd.clear(); //Muestro los resultados
      lcd.setCursor(0,0);
      lcd.print("Enviando ");
      lcd.setCursor(0,1);
      lcd.print("resultados");
      delay(2600);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("a");
      lcd.setCursor(0,1);
      lcd.print("Jugador B");
      delay(1600);
      lcd.clear();
      Serial.print(String(targetB));
      delay(1000);
      Serial.print(String(targetA));
    
    if (targetB>targetA){ //Comparaciones para saber quien gana la partida jugada
      lcd.setCursor(0,0);
      lcd.print("La partida");
      lcd.setCursor(0,1);
      lcd.print("la gano:");
      delay(2600);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Mr Python");
      lcd.setCursor(0,1);
      lcd.print("Jugador B");
      melodiaDerrota();
      delay(2600);
      scoreB++;
    }else if(targetB<targetA){
      lcd.setCursor(0,0);
      lcd.print("La partida");
      lcd.setCursor(0,1);
      lcd.print("la gano:");
      delay(2600);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Mr Arduino");
      lcd.setCursor(0,1);
      lcd.print("Jugador A");
      melodiaVictoria();
      delay(2600);
      scoreA++;
    }else{
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("La partida fue");
      lcd.setCursor(0,1);
      lcd.print("un empate");
      delay(2600);
    }
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("MostrandoPuntaje");
    lcd.setCursor(0,1);
    lcd.print("de la partida");
    delay(3500);
    lcd.clear();
    lcd.setCursor(0,0);
    targetA=targetA*100;
    targetB=targetB*100;
    lcd.print("Jugador A: "+(String)targetA);
    lcd.setCursor(0,1);
    lcd.print("Jugador B: "+(String)targetB);
    delay(4600);
  }else{
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("No esta diponible");
    delay(3600);
    }
    ronda = 0;
    targetB = 0;
    targetA = 0;
  }
  else{
     lcd.clear();
     lcd.setCursor(0,0);
     lcd.print("Ronda No:"+String(ronda+1));
     lcd.setCursor(0,1);
     lcd.print("TERMINADA");
     delay(3000);
     ronda++;
  }
}
  lcd.clear();
  /*****************/
  limpiarMatrizJA(1); //Limpio las matrices y los targets para la proxima partida
  limpiarMatrizJA(0);
  /******************/
  barcosLlenos = false;
  tirosLlenos = false;
  if(scoreA==2||scoreB==2) tmenu =0; //Ya alguno de los dos gana una partida, me salgo del menu del juego
}
