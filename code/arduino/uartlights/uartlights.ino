#include <AltSoftSerial.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

AltSoftSerial altSerial;
Adafruit_NeoPixel strip = null;

int     readCount = 0;
int     frameLength  = 0;
String  values = "";

void resetFrame(){
    readCount = 0;
    values.remove(0);
}

void discardPartial() {
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
}

void readFrameHeader(){
    nextChar = altSerial.read();
    if(frameLength == 0){               //frameLength was not previously set
        if(frameLength % 3 == 0){       //check it's divisible by 3
            frameLength = nextChar;     //store it
            //allocate string with enough bytes, including newline
            values.reserve(frameLength + 1);
            //allocate neopixel with enough pixels
            strip = Adafruit_NeoPixel(frameLength/3, PIN, NEO_GRB + NEO_KHZ800);
            Serial.print("Allocated NeoPixel with ");
            Serial.print(frameLength/3);
            Serial.println("pixels")
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
    uint32_t color;

    //populate colors from frame
    for(framePos = 0; framePos < frame; framePos += 3){
        color = strip.Color(values[framePos + 0], values[framePos + 1], values[framePos + 2])
        strip.setPixelColor(i, c);
    }

    //send to lights
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
            else if(nextChar == '\n'){  //byte after values should be newline
                processValues();
                resetFrame();
            }
            else{
                discardPartial();
                break;
            }

            readCount ++;
        }
    }
}