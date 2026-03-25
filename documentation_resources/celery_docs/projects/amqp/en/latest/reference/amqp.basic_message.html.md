<!-- Source: https://docs.celeryq.dev/projects/amqp/en/latest/reference/amqp.basic_message.html -->

This document is for py-amqp's development version, which can be
significantly different from previous releases. Get the stable docs here:
[5.3](https://amqp.readthedocs.io/en/latest/reference/amqp.basic_message.html).

# `amqp.basic_message`

AMQP Messages.

class amqp.basic\_message.Message(*body=''*, *children=None*, *channel=None*, *\*\*properties*)[[source]](../_modules/amqp/basic_message.html#Message)
:   A Message for use with the Channel.basic\_\* methods.

    Expected arg types

    > body: string
    > children: (not supported)

    Keyword properties may include:

    > content\_type: shortstr
    > :   MIME content type
    >
    > content\_encoding: shortstr
    > :   MIME content encoding
    >
    > application\_headers: table
    > :   Message header field table, a dict with string keys,
    >     and string | int | Decimal | datetime | dict values.
    >
    > delivery\_mode: octet
    > :   Non-persistent (1) or persistent (2)
    >
    > priority: octet
    > :   The message priority, 0 to 9
    >
    > correlation\_id: shortstr
    > :   The application correlation identifier
    >
    > reply\_to: shortstr
    > :   The destination to reply to
    >
    > expiration: shortstr
    > :   Message expiration specification
    >
    > message\_id: shortstr
    > :   The application message identifier
    >
    > timestamp: unsigned long
    > :   The message timestamp
    >
    > type: shortstr
    > :   The message type name
    >
    > user\_id: shortstr
    > :   The creating user id
    >
    > app\_id: shortstr
    > :   The creating application id
    >
    > cluster\_id: shortstr
    > :   Intra-cluster routing identifier
    >
    > Unicode bodies are encoded according to the ‘content\_encoding’
    > argument. If that’s None, it’s set to ‘UTF-8’ automatically.
    >
    > Example:
    >
    > ```
    > msg = Message('hello world',
    >                 content_type='text/plain',
    >                 application_headers={'foo': 7})
    > ```

    CLASS\_ID = 60

    PROPERTIES = [('content\_type', 's'), ('content\_encoding', 's'), ('application\_headers', 'F'), ('delivery\_mode', 'o'), ('priority', 'o'), ('correlation\_id', 's'), ('reply\_to', 's'), ('expiration', 's'), ('message\_id', 's'), ('timestamp', 'L'), ('type', 's'), ('user\_id', 's'), ('app\_id', 's'), ('cluster\_id', 's')]
    :   Instances of this class have these attributes, which
        are passed back and forth as message properties between
        client and server

    body

    channel

    delivery\_info
    :   set by basic\_consume/basic\_get

    property delivery\_tag

    property headers