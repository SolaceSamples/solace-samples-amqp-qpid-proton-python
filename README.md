# Getting Started Tutorials

## Using Apache Qpid Proton Python over AMQP 1.0 with Solace Message Routers

The Advanced Message Queuing Protocol (AMQP) is an open standard application layer protocol for message-oriented middleware, and Solace Message Routers support AMQP 1.0.

In addition to information provided on the Solace [Developer Portal](http://dev.solace.com/tech/amqp/), you may also look at external sources for more details about AMQP:

 - http://www.amqp.org
 - https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=amqp
 - http://docs.oasis-open.org/amqp/core/v1.0/amqp-core-complete-v1.0.pdf

The "Getting Started" tutorials will get you up to speed and sending messages with Solace technology as quickly as possible. There are three ways you can get started:

- Follow [these instructions](https://cloud.solace.com/create-messaging-service/) to quickly spin up a cloud-based Solace messaging service for your applications.
- Follow [these instructions](https://docs.solace.com/Solace-VMR-Set-Up/Setting-Up-VMRs.htm) to start the Solace VMR in leading Clouds, Container Platforms or Hypervisors. The tutorials outline where to download and how to install the Solace VMR.
- If your company has Solace message routers deployed, contact your middleware team to obtain the host name or IP address of a Solace message router to test against, a username and password to access it, and a VPN in which you can produce and consume messages.

## Contents

This repository contains code and matching tutorial walk throughs for basic Solace messaging patterns. For a nice introduction to the Solace API and associated tutorials, check out the [Getting Started Home Page](https://solacesamples.github.io/solace-samples-amqp-qpid-proton-python/).

See the individual tutorials for details:

- [Publish/Subscribe](https://solacesamples.github.io/solace-samples-amqp-qpid-jms1/publish-subscribe): Learn how to set up pub/sub messaging on a Solace VMR.

## Prerequisites

This tutorial requires the Apache Qpid Proton Python API library, version 0.22 (March 2018) or newer. Download the Proton Python API library to your computer from [here](https://qpid.apache.org/releases/).

## Build the Samples

Just clone and build. For example:

  1. clone this GitHub repository
  1. `./env.sh setup`

## Running the Samples

To try individual samples, build the project from source and then run samples like the following:

    ./env.sh run ./src/producer.py amqp://<msg_backbone_ip:port>

The individual tutorials linked above provide full details which can walk you through the samples, what they do, and how to correctly run them to explore Solace messaging.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

See the list of [contributors](https://github.com/SolaceSamples/solace-samples-amqp-qpid-proton-python/contributors) who participated in this project.

## License

This project is licensed under the Apache License, Version 2.0. - See the [LICENSE](LICENSE) file for details.

## Resources

For more information try these resources:

- The Solace Developer Portal website at: http://dev.solace.com
- Get a better understanding of [Solace technology](http://dev.solace.com/tech/).
- Check out the [Solace blog](http://dev.solace.com/blog/) for other interesting discussions around Solace technology
- Ask the [Solace community.](http://dev.solace.com/community/)
