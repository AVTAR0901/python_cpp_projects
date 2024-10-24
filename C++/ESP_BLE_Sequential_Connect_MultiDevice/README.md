# Read ME

## ESP32 multiple connection using BLE network (Sequential connect)

- The Client in this code connects to atmost 6 server ESPs
- Minimum of 1 server can be connected and get data and max 6
- Client here sequentially connects to servers one at time, gives data, disconnects. One cycle of getting data of all sensors takes less then 5 seconds
- in Server while coding make sure commment out the lines that are not the server sepcific, have mentioned all clearly
