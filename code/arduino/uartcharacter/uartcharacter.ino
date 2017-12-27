#include <Adafruit_NeoPixel.h>
//#ifdef __AVR__
//  #include <avr/power.h>
//#endif

#define NEOPIXEL_PIN A3
#define BYTES_PER_PIXEL 3

boolean segmentCountRead = false;

Adafruit_NeoPixel strip = NULL; //not initialised until first frame header arrives
int     segmentCount  = 0;
int     segmentLength = 12;
int     segmentPos    = 0;

uint8_t colorVals[BYTES_PER_PIXEL];
int     colorPos = 0;

void resetFrame(){
  segmentCountRead = false;
  segmentPos = 0;
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

boolean readSegmentCount(){
    char nextChar = Serial.read();
    if(segmentCount== 0){                 //segmentCount was not previously set
      segmentCount = (int)nextChar;     //store it
      Serial.print(F("NewCount:"));
      Serial.println(segmentCount);
      //construct neopixel with enough pixels, and begin it
      //strip = Adafruit_NeoPixel(segmentCount * segmentLength, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
      strip = Adafruit_NeoPixel(196, NEOPIXEL_PIN, NEO_RGB + NEO_KHZ800);
      strip.begin();
      segmentCountRead = true;
    }
    else if (nextChar == segmentCount){ //check frameLength matches
      Serial.println(F("OldCount"));
      segmentCountRead = true;
    }
    else{
      //fallthrough to error state
      Serial.println(F("Corrupt"));
      segmentCountRead = false;
    }
    return segmentCountRead;
}

void setup() {
  Serial.begin(115200);
  discardPartial();
}

void setSegmentColor(int segmentPos, uint8_t red, uint8_t green, uint8_t blue){
  int lower = segmentPos * segmentLength;
  if(segmentPos > 0){ // calculate offset for idle pixels
    lower += ((segmentPos - 1) / 4) + 1;
  }
  int upper = lower + segmentLength;
  int pixelPos;
  for(pixelPos = lower; pixelPos < upper; pixelPos ++){
    strip.setPixelColor(pixelPos, red, green, blue);
  } 
}

void loop() {
    int headerLength;
    char nextChar;

    while(Serial.available()){
        if( ! segmentCountRead ){ //try to read first byte as 'segmentCount' header
          readSegmentCount();
          if( ! segmentCountRead ){ //pi
              discardPartial();
              break;
          }
        }
        else{
            nextChar = Serial.read();

            if(segmentPos < segmentCount){ //subsequent non-terminal bytes are values
                colorVals[colorPos] = (uint8_t)nextChar;
                colorPos ++;
                if(colorPos == BYTES_PER_PIXEL){
                  setSegmentColor(segmentPos, colorVals[0], colorVals[1], colorVals[2]);
                  segmentPos++;
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
