<!-- Source: https://docs.celeryq.dev/projects/amqp/en/latest/reference/amqp.abstract_channel.html -->

This document is for py-amqp's development version, which can be
significantly different from previous releases. Get the stable docs here:
[5.3](https://amqp.readthedocs.io/en/latest/reference/amqp.abstract_channel.html).

# `amqp.abstract_channel`

Code common to Connection and Channel objects.

class amqp.abstract\_channel.AbstractChannel(*connection*, *channel\_id*)[[source]](../_modules/amqp/abstract_channel.html#AbstractChannel)
:   Superclass for Connection and Channel.

    The connection is treated as channel 0, then comes
    user-created channel objects.

    The subclasses must have a \_METHOD\_MAP class property, mapping
    between AMQP method signatures and Python methods.

    auto\_decode

    channel\_id

    close()[[source]](../_modules/amqp/abstract_channel.html#AbstractChannel.close)
    :   Close this Channel or Connection.

    connection

    dispatch\_method(*method\_sig*, *payload*, *content*)[[source]](../_modules/amqp/abstract_channel.html#AbstractChannel.dispatch_method)

    is\_closing

    method\_queue

    send\_method(*sig*, *format=None*, *args=None*, *content=None*, *wait=None*, *callback=None*, *returns\_tuple=False*)[[source]](../_modules/amqp/abstract_channel.html#AbstractChannel.send_method)

    wait(*method*, *callback=None*, *timeout=None*, *returns\_tuple=False*)[[source]](../_modules/amqp/abstract_channel.html#AbstractChannel.wait)