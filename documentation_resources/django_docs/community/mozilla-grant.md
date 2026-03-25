<!-- Source: https://www.django-rest-framework.org/community/mozilla-grant -->

# Mozilla Grant

We have recently been [awarded a Mozilla grant](https://blog.mozilla.org/blog/2016/04/13/mozilla-open-source-support-moss-update-q1-2016/), in order to fund the next major releases of REST framework. This work will focus on seamless client-side integration by introducing supporting client libraries that are able to dynamically interact with REST framework APIs. The framework will provide for either hypermedia or schema endpoints, which will expose the available interface for the client libraries to interact with.

Additionally, we will be building on the realtime support that Django Channels provides, supporting and documenting how to build realtime APIs with REST framework. Again, this will include supporting work in the associated client libraries, making it easier to build richly interactive applications.

The [Core API](https://www.coreapi.org/) project will provide the foundations for our client library support, and will allow us to support interaction using a wide range of schemas and hypermedia formats. It's worth noting that these client libraries won't be tightly coupled to solely REST framework APIs either, and will be able to interact with *any* API that exposes a supported schema or hypermedia format.

Specifically, the work includes:

## Client libraries

This work will include built-in schema and hypermedia support, allowing dynamic client libraries to interact with the API. I'll also be releasing both Python and Javascript client libraries, plus a command-line client, a new tutorial section, and further documentation.

- Client library support in REST framework.
- Schema & hypermedia support for REST framework APIs.
- A test client, allowing you to write tests that emulate a client library interacting with your API.
- New tutorial sections on using client libraries to interact with REST framework APIs.
- Python client library.
- JavaScript client library.
- Command line client.

## Realtime APIs

The next goal is to build on the realtime support offered by Django Channels, adding support & documentation for building realtime API endpoints.

- Support for API subscription endpoints, using REST framework and Django Channels.
- New tutorial section on building realtime API endpoints with REST framework.
- Realtime support in the Python & Javascript client libraries.

## Accountability

In order to ensure that I can be fully focused on trying to secure a sustainable
& well-funded open source business I will be leaving my current role at [DabApps](https://www.dabapps.com/)
at the end of May 2016.

I have formed a UK limited company, [Encode](https://www.encode.io/), which will
act as the business entity behind REST framework. I will be issuing monthly reports
from Encode on progress both towards the Mozilla grant, and for development time
funded via the REST framework paid plans.

## Stay up to date, with our monthly progress reports...

Email Address

Back to top