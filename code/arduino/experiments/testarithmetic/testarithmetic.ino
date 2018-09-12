int numSegments = 16;
int segmentLength = 12;

void setup() {
  Serial.begin(115200);
  for(int i = 0; i < numSegments; i++){
    printSegment(i);
  }
}

void printSegment(int segmentPos){
  int lower = segmentPos * segmentLength;
  int offset = 0;
  if(segmentPos > 0){ // calculate offset for idle pixels
    offset = ((segmentPos - 1) / 4) + 1;
  }
  lower += offset;
  int upper = lower + segmentLength;
  Serial.print("Segment");
  Serial.print(segmentPos);
  Serial.print(" bounds ");
  Serial.print(lower);
  Serial.print(", ");
  Serial.println(upper);
}


void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < numSegments; i++){
      printSegment(i);
  }
}
