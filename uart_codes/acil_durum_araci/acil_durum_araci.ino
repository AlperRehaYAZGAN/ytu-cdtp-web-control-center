uint8_t led_a = 7;
uint8_t led_b = 8;
#define PACKETSIZE  7
uint8_t packet[PACKETSIZE];

union crcConverter{
  uint32_t fullData;
  uint8_t bytes[4];
}crcConverter;

uint32_t crcCheck(uint8_t *message, size_t l);

void setup() {
  Serial.begin(9600);
  pinMode(led_a, OUTPUT);
  pinMode(led_b, OUTPUT);
}

void loop() { 
 if (Serial.available() > 0) {
  Serial.readBytes(packet, PACKETSIZE);
  if((packet[0] == 4) and (packet[1] == 5)){
    if(crcCheck(packet, 7) == 0){
      if(packet[2] < 2 ){
        digitalWrite(led_a, packet[2]);
        delay(200);
      }
      else if((packet[2] > 1) && (packet[2] < 4)){
        digitalWrite(led_b, packet[2]-2);
        delay(200);
      }
      else{
        digitalWrite(led_a, LOW);
        digitalWrite(led_b, LOW);
      }
    }
  }
  else{
    Serial.read();
    Serial.flush();
  }
 }
  
}

uint32_t crcCheck(uint8_t *message, size_t l){
   uint32_t crc, msb;
   uint8_t err = 0;
   crc = 0xFFFFFFFF;

   for(uint8_t i = 0; i < 4; i++){
     crcConverter.bytes[i] = message[l + i];
   }

   for(size_t i = 0; i < l; i++) {
      // xor next byte to upper bits of crc
      crc ^= (((uint32_t)message[i])<<24);
      for (uint8_t j = 0; j < 8; j++) {    // Do eight times.
            msb = crc>>31;
            crc <<= 1;
            crc ^= (0 - msb) & 0x04C11DB7;
      }
   }

   return crc;

}
