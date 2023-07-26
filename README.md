# rabbitmq\_head\_message\_timestamp\_exporter

## Overview

This is a small proof-of-concept tool to obtain the timestamps of the
last OpenStack notification messages, by type, sent to Ceilometer.

The idea is to be able to write prometheus alerts if the Ceilometer
queues are suspiciously quiet, in particular when polling events are
not coming in as expected.

## Usage

See the corresponding help outputs:

```console
$ mqmon.py -h
```

```console
$ mqmon_exporter.py -h
```

