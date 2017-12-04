#include <AltSoftSerial.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define NEOPIXEL_PIN 6

AltSoftSerial altSerial;
Adafruit_NeoPixel strip = NULL; //not initialised until first frame header arrives

int     readCount = 0;
int     frameLength  = 0;
int     chainLength = 16;
String  values = "";

void resetFrame(){
    readCount = 0;
    values.remove(0);
}

void discardPartial() {
    char c;
    //consumes serial bytes until buffered partial line discarded
    while(true){
        if (altSerial.available()) {
            c = altSerial.read();
            if(c=='\n'){
                break;
            }
        }
    }
    resetFrame();
    Serial.println("Discarded and Reset");
}

int readFrameHeader(){
    char nextChar = altSerial.read();
    if(frameLength == 0){               //frameLength was not previously set
        if(frameLength % 3 == 0){       //consistency check it's divisible by 3
            frameLength = nextChar;     //store it
            //allocate string with enough bytes, including newline
            values.reserve(frameLength + 1);
            Serial.print("Received FrameLength");
            Serial.println(frameLength);
            //construct neopixel with enough pixels, and begin it
//            strip = Adafruit_NeoPixel(frameLength/3, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
            strip = Adafruit_NeoPixel(chainLength, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
            strip.begin();
            Serial.print("Allocated NeoPixel with ");
            Serial.print(frameLength/3);
            Serial.println("pixels");
            return 1;
        }
    }
    else if (nextChar == frameLength ){ //check frameLength matches
        Serial.println("Frame size correct");
        return 1;
    }

    //fallthrough to error state
    Serial.println("Frame size changed or serial corrupted");
    return 0;
}

void processValues(){
    int framePos;
    int pixelPos;

    //populate colors from frame
    for(framePos = 0; framePos < frameLength; framePos += 3){
        pixelPos = framePos / 3;
        /*
        Serial.print("Pix:");
        Serial.println(pixelPos);
        Serial.print("Color:(");
        Serial.print((uint8_t)values[framePos + 0]);
        Serial.print(",");
        Serial.print((uint8_t)values[framePos + 1]);
        Serial.print(",");
        Serial.print((uint8_t)values[framePos + 2]);
        Serial.println(")");
        */
        strip.setPixelColor(pixelPos, (uint8_t)values[framePos + 0], (uint8_t)values[framePos + 1], (uint8_t)values[framePos + 2]);
    }

    /*
    for(pixelPos = 0; pixelPos < chainLength; pixelPos++){
        strip.setPixelColor(pixelPos, 0, 255, 0);      
    }
    */
  
    //send to lights
    Serial.println("Sending to lights");
    strip.show();
}

void setup() {
  Serial.begin(57600);
  altSerial.begin(57600);
  discardPartial();
}

void loop() {
    int headerLength;
    char nextChar;

    while(altSerial.available()){
        if(readCount == 0){   //first byte is header
            headerLength = readFrameHeader();

            if(headerLength == 0){
                discardPartial();
                break;
            }

            readCount += headerLength;
        }
        else{
            nextChar = altSerial.read();

            if(readCount - headerLength < frameLength ){ //subsequent non-terminal bytes are values
                values += nextChar;
            }
            else if(nextChar == '\n'){  //trailing byte after frame should be newline
                Serial.println("Complete: processing");
                processValues();
                resetFrame();
            }
            else{                       //trailing byte after frame not newline
                Serial.println("Surplus; discarding");
                discardPartial();
                break;
            }

            readCount ++;
        }
    }
}
