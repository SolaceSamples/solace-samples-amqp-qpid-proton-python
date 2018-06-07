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
This repository contains sample code for the following scenarios:

1. Publish to a Queue, see [simple_send](src/simple_send.py)
2. Receive from a Queue, see [simple_recv](src/simple_recv.py)
3. Publish on a Topic using address prefix, see [producer](src/producer.py)
4. Receive from Durable Topic Endpoint using address prefix, see [consumer](src/dte_consumer.py)
5. Receive from Durable Topic Endpoint using address prefix and terminus durability fields, see [consumer_std](src/dte_consumer_std.py)

>**Note** AMQP address prefixes are not supported until Solace PubSub+ Software Message Broker **version 8.11.0** and Solace PubSub+ Message Broker **version 8.5.0**.

## Prerequisites

Must have python 2.7 or later installed and available.
Must have bash shell script environment.

## Building & Running

### Activate environment and run the Examples

Just clone and activate. For example:

  1. clone this GitHub repository
  2. `source ./env.sh activate`

### Running the Examples

To try individual examples, build the project from source and then run them like the following:

    python src/simple_send.py amqp://<msg_backbone_ip:port>

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

See the list of [contributors](https://github.com/SolaceSamples/solace-samples-amqp-qpid-proton-python/graphs/contributors) who participated in this project.

## License

This project is licensed under the Apache License, Version 2.0. - See the [LICENSE](LICENSE) file for details.

## Resources

For more information try these resources:

- The Solace Developer Portal website at: http://dev.solace.com
- Get a better understanding of [Solace technology](http://dev.solace.com/tech/).
- Check out the [Solace blog](http://dev.solace.com/blog/) for other interesting discussions around Solace technology
- Ask the [Solace community.](http://dev.solace.com/community/)
