# AB-Sens-Tactile-Sensor

## Overview

Tactile Sensors' coding examples.

Visit [AB-Sens](https://ab-sens.com) for more information about the sensors.

### License

The source code is released under a [BSD 3-Clause license](AB-Sens-Tactile-Sensor/LICENSE).

**Author: Alexandre Bernier<br />
Affiliation: [AB-Sens](http://ab-sens.com)<br />
Maintainer: Alexandre Bernier, alexandre@ab-sens.com**

All these examples have been tested on Ubuntu 22.04.

## Usage

### Communication

#### Message structure

All messages (in or out) follow the same structure as described below:

| Byte | Description    |    Value    |
|:----:|----------------|:-----------:|
|  0   | Start byte     |   `0x9A`    |
|  1   | Not used       |   Ignored   |
|  2   | Command        | *See below* |
|  3   | Length of data |   Varies    |
|  4+  | Data           | *See below* |

#### Commands

Here's a list of all available commands:

| Value  | Command                   | Parameter                    | Parameter size |     
|:------:|---------------------------|------------------------------|:--------------:|
| `0x58` | Auto send sensor values   | Period between messages (ms) |     1 byte     |
| `0x61` | Read sensor values (once) | None                         |     0 byte     |

#### Write (sending commands)

Which command you send will determine if you need to send data with the message or not.

When sending "Read sensor values (once)" to the tactile sensor, no data is necessary in the message. You can thus put
`0` as the Length of data. An example of a message asking the tactile sensor to send a single burst of values would
look like this:

*Command = Read sensor values (once)*

| First byte | Not used | Command | Length of data |
|:----------:|:--------:|:-------:|:--------------:|
|   `0x9A`   |  `0x00`  | `0x61`  |     `0x00`     |

When sending "Auto send sensor values" to the tactile sensor, you need to add a byte of data containing the period
you want between each data point. An example of a message asking the tactile sensor to auto send values every
1ms would look like this:

*Command = Auto send sensor values*

| First byte | Not used | Command | Length of data |  Data   |
|:----------:|:--------:|:-------:|:--------------:|:-------:|
|   `0x9A`   |  `0x00`  | `0x58`  |     `0x01`     | `0x01`  |

#### Read (receiving data)
When receiving a response from the tactile sensor, the message header will follow the same structure as above.
Regardless of which command you sent, the response will always have `0x61` as the command byte.

Within the data bytes that follow, there will always be a byte that indicates what kind of values you are reading.
That preceding byte is split into two values. The four most significant bits (MSB) will tell the kind of values you are
reading; while the four least significant bits (LSB) will tell which finger the data is coming from. 

Here's a list of all the sensor types you will receive for each finger (if both are connected) and the amount of bytes
that will follow each sensor type:

| Sensor type     | Finger 0 | Finger 1 | Number of bytes                               |     
|-----------------|----------|----------|-----------------------------------------------|
| Static tactile  | `0x10`   | `0x14`   | 56 bytes *(28 static taxels * 2 bytes/taxel)* |
| Dynamic tactile | `0x20`   | `0x24`   | 2 bytes *(1 dynamic taxel * 2 bytes/taxel)*   |
| Accelerometer   | `0x30`   | `0x34`   | 6 bytes *(3 axes * 2 bytes/axis)*             |
| Gyroscope       | `0x40`   | `0x44`   | 6 bytes *(3 axes * 2 bytes/axis)*             |

Even though there are 8 different sensor types you can receive, all these data bytes will be split into 3 different
messages: one for finger 0 static tactile data; one for finger 1 static tactile data; and one last message for
everything else.

## Examples

### Python

Please refer to the [Python README](Examples/Python/Python_README.md).

## Bugs & Feature Requests

Please report bugs and request features using the [Issue Tracker](https://github.com/alexandre-bernier/AB-Sens-Tactile-Sensor/issues).
