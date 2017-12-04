#include <Adafruit_NeoPixel.h>
//#ifdef __AVR__
//  #include <avr/power.h>
//#endif

#define NEOPIXEL_PIN 6
#define BYTES_PER_PIXEL 3

boolean pixelCountRead = false;

Adafruit_NeoPixel strip = NULL; //not initialised until first frame header arrives
int     pixelCount  = 0;
int     pixelPos    = 0;

uint8_t colorVals[BYTES_PER_PIXEL];
int     colorPos = 0;

void resetFrame(){
  pixelCountRead = false;
  pixelPos = 0;
  colorPos = 0;
}

void discardPartial() {
    char c;
    //consumes serial bytes until buffered partial line discarded
    while(true){
        if (Serial.available()) {
            c = Serial.read();
            if(c=='\n'){
                break;
            }
        }
    }
    resetFrame();
    Serial.println(F("Discard"));
}

boolean readPixelCount(){
    char nextChar = Serial.read();
    if(pixelCount== 0){                 //pixelCount was not previously set
      pixelCount = (int)nextChar;     //store it
      Serial.print(F("NewCount:"));
      Serial.println(pixelCount);
      //construct neopixel with enough pixels, and begin it
      //strip = Adafruit_NeoPixel(pixelCount, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
      strip = Adafruit_NeoPixel(192, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
      strip.begin();
      pixelCountRead = true;
    }
    else if (nextChar == pixelCount){ //check frameLength matches
      Serial.println(F("OldCount"));
      pixelCountRead = true;
    }
    else{
      //fallthrough to error state
      Serial.println(F("Corrupt"));
      pixelCountRead = false;
    }
    return pixelCountRead;
}

void setup() {
  Serial.begin(115200);
  discardPartial();
}

void loop() {
    int headerLength;
    char nextChar;

    while(Serial.available()){
        if( ! pixelCountRead ){ //try to read first byte as 'pixelCount' header
          readPixelCount();
          if( ! pixelCountRead ){ //pi
              discardPartial();
              break;
          }
        }
        else{
            nextChar = Serial.read();

            if(pixelPos < pixelCount){ //subsequent non-terminal bytes are values
                colorVals[colorPos] = (uint8_t)nextChar;
                colorPos ++;
                if(colorPos == BYTES_PER_PIXEL){
                  strip.setPixelColor(pixelPos, colorVals[0], colorVals[1], colorVals[2]);
                  pixelPos++;
                  colorPos = 0;
                }
            }
            else if(nextChar == '\n'){  //trailing byte after frame should be newline
                Serial.println(F("Show"));
                strip.show();
                resetFrame();
            }
            else{                       //trailing byte after frame not newline
                Serial.println(F("Surplus"));
                discardPartial();
                break;
            }
        }
    }
}
