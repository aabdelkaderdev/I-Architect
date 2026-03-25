<!-- Source: https://docs.celeryq.dev/projects/amqp/en/latest/reference/amqp.channel.html -->

This document is for py-amqp's development version, which can be
significantly different from previous releases. Get the stable docs here:
[5.3](https://amqp.readthedocs.io/en/latest/reference/amqp.channel.html).

# `amqp.channel`

AMQP Channels.

class amqp.channel.Channel(*connection*, *channel\_id=None*, *auto\_decode=True*, *on\_open=None*)[[source]](../_modules/amqp/channel.html#Channel)
:   AMQP Channel.

    The channel class provides methods for a client to establish a
    virtual connection - a channel - to a server and for both peers to
    operate the virtual connection thereafter.

    GRAMMAR:

    ```
    channel             = open-channel *use-channel close-channel
    open-channel        = C:OPEN S:OPEN-OK
    use-channel         = C:FLOW S:FLOW-OK
                        / S:FLOW C:FLOW-OK
                        / functional-class
    close-channel       = C:CLOSE S:CLOSE-OK
                        / S:CLOSE C:CLOSE-OK
    ```

    Create a channel bound to a connection and using the specified
    numeric channel\_id, and open on the server.

    The ‘auto\_decode’ parameter (defaults to True), indicates
    whether the library should attempt to decode the body
    of Messages to a Unicode string if there’s a ‘content\_encoding’
    property for the message. If there’s no ‘content\_encoding’
    property, or the decode raises an Exception, the message body
    is left as plain bytes.

    auto\_decode

    basic\_ack(*delivery\_tag*, *multiple=False*, *argsig='Lb'*)[[source]](../_modules/amqp/channel.html#Channel.basic_ack)
    :   Acknowledge one or more messages.

        This method acknowledges one or more messages delivered via
        the Deliver or Get-Ok methods. The client can ask to confirm
        a single message or a set of messages up to and including a
        specific message.

        PARAMETERS:
        :   delivery\_tag: longlong

            > server-assigned delivery tag
            >
            > The server-assigned and channel-specific delivery tag
            >
            > RULE:
            >
            > > The delivery tag is valid only within the channel
            > > from which the message was received. I.e. a client
            > > MUST NOT receive a message on one channel and then
            > > acknowledge it on another.
            >
            > RULE:
            >
            > > The server MUST NOT use a zero value for delivery
            > > tags. Zero is reserved for client use, meaning “all
            > > messages so far received”.

            multiple: boolean

            > acknowledge multiple messages
            >
            > If set to True, the delivery tag is treated as “up to
            > and including”, so that the client can acknowledge
            > multiple messages with a single method. If set to
            > False, the delivery tag refers to a single message.
            > If the multiple field is True, and the delivery tag
            > is zero, tells the server to acknowledge all
            > outstanding messages.
            >
            > RULE:
            >
            > > The server MUST validate that a non-zero delivery-
            > > tag refers to an delivered message, and raise a
            > > channel exception if this is not the case.

    basic\_cancel(*consumer\_tag*, *nowait=False*, *argsig='sb'*)[[source]](../_modules/amqp/channel.html#Channel.basic_cancel)
    :   End a queue consumer.

        This method cancels a consumer. This does not affect already
        delivered messages, but it does mean the server will not send
        any more messages for that consumer. The client may receive
        an arbitrary number of messages in between sending the cancel
        method and receiving the cancel-ok reply.

        RULE:

        > If the queue no longer exists when the client sends a
        > cancel command, or the consumer has been cancelled for
        > other reasons, this command has no effect.

        PARAMETERS:
        :   consumer\_tag: shortstr

            > consumer tag
            >
            > Identifier for the consumer, valid within the current
            > connection.
            >
            > RULE:
            >
            > > The consumer tag is valid only within the channel
            > > from which the consumer was created. I.e. a client
            > > MUST NOT create a consumer in one channel and then
            > > use it in another.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

    basic\_consume(*queue=''*, *consumer\_tag=''*, *no\_local=False*, *no\_ack=False*, *exclusive=False*, *nowait=False*, *callback=None*, *arguments=None*, *on\_cancel=None*, *argsig='BssbbbbF'*)[[source]](../_modules/amqp/channel.html#Channel.basic_consume)
    :   Start a queue consumer.

        This method asks the server to start a “consumer”, which is a
        transient request for messages from a specific queue.
        Consumers last as long as the channel they were created on, or
        until the client cancels them.

        RULE:

        > The server SHOULD support at least 16 consumers per queue,
        > unless the queue was declared as private, and ideally,
        > impose no limit except as defined by available resources.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to consume from. If
            > the queue name is null, refers to the current queue
            > for the channel, which is the last declared queue.
            >
            > RULE:
            >
            > > If the client did not previously declare a queue,
            > > and the queue name in this method is empty, the
            > > server MUST raise a connection exception with
            > > reply code 530 (not allowed).

            consumer\_tag: shortstr

            > Specifies the identifier for the consumer. The
            > consumer tag is local to a connection, so two clients
            > can use the same consumer tags. If this field is empty
            > the server will generate a unique tag.
            >
            > RULE:
            >
            > > The tag MUST NOT refer to an existing consumer. If
            > > the client attempts to create two consumers with
            > > the same non-empty tag the server MUST raise a
            > > connection exception with reply code 530 (not
            > > allowed).

            no\_local: boolean

            > do not deliver own messages
            >
            > If the no-local field is set the server will not send
            > messages to the client that published them.

            no\_ack: boolean

            > no acknowledgment needed
            >
            > If this field is set the server does not expect
            > acknowledgments for messages. That is, when a message
            > is delivered to the client the server automatically and
            > silently acknowledges it on behalf of the client. This
            > functionality increases performance but at the cost of
            > reliability. Messages can get lost if a client dies
            > before it can deliver them to the application.

            exclusive: boolean

            > request exclusive access
            >
            > Request exclusive consumer access, meaning only this
            > consumer can access the queue.
            >
            > RULE:
            >
            > > If the server cannot grant exclusive access to the
            > > queue when asked, - because there are other
            > > consumers active - it MUST raise a channel
            > > exception with return code 403 (access refused).

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

            callback: Python callable

            > function/method called with each delivered message
            >
            > For each message delivered by the broker, the
            > callable will be called with a Message object
            > as the single argument. If no callable is specified,
            > messages are quietly discarded, no\_ack should probably
            > be set to True in that case.

    basic\_get(*queue=''*, *no\_ack=False*, *argsig='Bsb'*)[[source]](../_modules/amqp/channel.html#Channel.basic_get)
    :   Direct access to a queue.

        This method provides a direct access to the messages in a
        queue using a synchronous dialogue that is designed for
        specific types of application where synchronous functionality
        is more important than performance.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to consume from. If
            > the queue name is null, refers to the current queue
            > for the channel, which is the last declared queue.
            >
            > RULE:
            >
            > > If the client did not previously declare a queue,
            > > and the queue name in this method is empty, the
            > > server MUST raise a connection exception with
            > > reply code 530 (not allowed).

            no\_ack: boolean

            > no acknowledgment needed
            >
            > If this field is set the server does not expect
            > acknowledgments for messages. That is, when a message
            > is delivered to the client the server automatically and
            > silently acknowledges it on behalf of the client. This
            > functionality increases performance but at the cost of
            > reliability. Messages can get lost if a client dies
            > before it can deliver them to the application.

        Non-blocking, returns a amqp.basic\_message.Message object,
        or None if queue is empty.

    basic\_publish(*msg*, *exchange=''*, *routing\_key=''*, *mandatory=False*, *immediate=False*, *timeout=None*, *confirm\_timeout=None*, *argsig='Bssbb'*)
    :   Publish a message.

        This method publishes a message to a specific exchange. The
        message will be routed to queues as defined by the exchange
        configuration and distributed to any active consumers when the
        transaction, if any, is committed.

        When channel is in confirm mode (when Connection parameter
        confirm\_publish is set to True), each message is confirmed.
        When broker rejects published message (e.g. due internal broker
        constrains), MessageNacked exception is raised and
        set confirm\_timeout to wait maximum confirm\_timeout second
        for message to confirm.

        PARAMETERS:
        :   exchange: shortstr

            > Specifies the name of the exchange to publish to. The
            > exchange name can be empty, meaning the default
            > exchange. If the exchange name is specified, and that
            > exchange does not exist, the server will raise a
            > channel exception.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to
            > > mean the default exchange.
            >
            > RULE:
            >
            > > The exchange MAY refuse basic content in which
            > > case it MUST raise a channel exception with reply
            > > code 540 (not implemented).

            routing\_key: shortstr

            > Message routing key
            >
            > Specifies the routing key for the message. The
            > routing key is used for routing messages depending on
            > the exchange configuration.

            mandatory: boolean

            > indicate mandatory routing
            >
            > This flag tells the server how to react if the message
            > cannot be routed to a queue. If this flag is True, the
            > server will return an unroutable message with a Return
            > method. If this flag is False, the server silently
            > drops the message.
            >
            > RULE:
            >
            > > The server SHOULD implement the mandatory flag.

            immediate: boolean

            > request immediate delivery
            >
            > This flag tells the server how to react if the message
            > cannot be routed to a queue consumer immediately. If
            > this flag is set, the server will return an
            > undeliverable message with a Return method. If this
            > flag is zero, the server will queue the message, but
            > with no guarantee that it will ever be consumed.
            >
            > RULE:
            >
            > > The server SHOULD implement the immediate flag.

            timeout: short

            > timeout for publish
            >
            > Set timeout to wait maximum timeout second
            > for message to publish.

            confirm\_timeout: short

            > confirm\_timeout for publish in confirm mode
            >
            > When the channel is in confirm mode set
            > confirm\_timeout to wait maximum confirm\_timeout
            > second for message to confirm.

    basic\_publish\_confirm(*\*args*, *\*\*kwargs*)[[source]](../_modules/amqp/channel.html#Channel.basic_publish_confirm)

    basic\_qos(*prefetch\_size*, *prefetch\_count*, *a\_global*, *argsig='lBb'*)[[source]](../_modules/amqp/channel.html#Channel.basic_qos)
    :   Specify quality of service.

        This method requests a specific quality of service. The QoS
        can be specified for the current channel or for all channels
        on the connection. The particular properties and semantics of
        a qos method always depend on the content class semantics.
        Though the qos method could in principle apply to both peers,
        it is currently meaningful only for the server.

        PARAMETERS:
        :   prefetch\_size: long

            > prefetch window in octets
            >
            > The client can request that messages be sent in
            > advance so that when the client finishes processing a
            > message, the following message is already held
            > locally, rather than needing to be sent down the
            > channel. Prefetching gives a performance improvement.
            > This field specifies the prefetch window size in
            > octets. The server will send a message in advance if
            > it is equal to or smaller in size than the available
            > prefetch size (and also falls into other prefetch
            > limits). May be set to zero, meaning “no specific
            > limit”, although other prefetch limits may still
            > apply. The prefetch-size is ignored if the no-ack
            > option is set.
            >
            > RULE:
            >
            > > The server MUST ignore this setting when the
            > > client is not processing any messages - i.e. the
            > > prefetch size does not limit the transfer of
            > > single messages to a client, only the sending in
            > > advance of more messages while the client still
            > > has one or more unacknowledged messages.

            prefetch\_count: short

            > prefetch window in messages
            >
            > Specifies a prefetch window in terms of whole
            > messages. This field may be used in combination with
            > the prefetch-size field; a message will only be sent
            > in advance if both prefetch windows (and those at the
            > channel and connection level) allow it. The prefetch-
            > count is ignored if the no-ack option is set.
            >
            > RULE:
            >
            > > The server MAY send less data in advance than
            > > allowed by the client’s specified prefetch windows
            > > but it MUST NOT send more.

            a\_global: boolean

            > Defines a scope of QoS. Semantics of this parameter differs
            > between AMQP 0-9-1 standard and RabbitMQ broker:
            >
            > MEANING IN AMQP 0-9-1:
            > :   False: shared across all consumers on the channel
            >     True: shared across all consumers on the connection
            >
            > MEANING IN RABBITMQ:
            > :   False: applied separately to each new consumer
            >     :   on the channel
            >
            >     True: shared across all consumers on the channel

    basic\_recover(*requeue=False*)[[source]](../_modules/amqp/channel.html#Channel.basic_recover)
    :   Redeliver unacknowledged messages.

        This method asks the broker to redeliver all unacknowledged
        messages on a specified channel. Zero or more messages may be
        redelivered. This method is only allowed on non-transacted
        channels.

        RULE:

        > The server MUST set the redelivered flag on all messages
        > that are resent.

        RULE:

        > The server MUST raise a channel exception if this is
        > called on a transacted channel.

        PARAMETERS:
        :   requeue: boolean

            > requeue the message
            >
            > If this field is False, the message will be redelivered
            > to the original recipient. If this field is True, the
            > server will attempt to requeue the message,
            > potentially then delivering it to an alternative
            > subscriber.

    basic\_recover\_async(*requeue=False*)[[source]](../_modules/amqp/channel.html#Channel.basic_recover_async)

    basic\_reject(*delivery\_tag*, *requeue*, *argsig='Lb'*)[[source]](../_modules/amqp/channel.html#Channel.basic_reject)
    :   Reject an incoming message.

        This method allows a client to reject a message. It can be
        used to interrupt and cancel large incoming messages, or
        return untreatable messages to their original queue.

        RULE:

        > The server SHOULD be capable of accepting and process the
        > Reject method while sending message content with a Deliver
        > or Get-Ok method. I.e. the server should read and process
        > incoming methods while sending output frames. To cancel a
        > partially-send content, the server sends a content body
        > frame of size 1 (i.e. with no data except the frame-end
        > octet).

        RULE:

        > The server SHOULD interpret this method as meaning that
        > the client is unable to process the message at this time.

        RULE:

        > A client MUST NOT use this method as a means of selecting
        > messages to process. A rejected message MAY be discarded
        > or dead-lettered, not necessarily passed to another
        > client.

        PARAMETERS:
        :   delivery\_tag: longlong

            > server-assigned delivery tag
            >
            > The server-assigned and channel-specific delivery tag
            >
            > RULE:
            >
            > > The delivery tag is valid only within the channel
            > > from which the message was received. I.e. a client
            > > MUST NOT receive a message on one channel and then
            > > acknowledge it on another.
            >
            > RULE:
            >
            > > The server MUST NOT use a zero value for delivery
            > > tags. Zero is reserved for client use, meaning “all
            > > messages so far received”.

            requeue: boolean

            > requeue the message
            >
            > If this field is False, the message will be discarded.
            > If this field is True, the server will attempt to
            > requeue the message.
            >
            > RULE:
            >
            > > The server MUST NOT deliver the message to the
            > > same client within the context of the current
            > > channel. The recommended strategy is to attempt
            > > to deliver the message to an alternative consumer,
            > > and if that is not possible, to move the message
            > > to a dead-letter queue. The server MAY use more
            > > sophisticated tracking to hold the message on the
            > > queue and redeliver it to the same client at a
            > > later stage.

    channel\_id

    close(*reply\_code=0*, *reply\_text=''*, *method\_sig=(0, 0)*, *argsig='BsBB'*)[[source]](../_modules/amqp/channel.html#Channel.close)
    :   Request a channel close.

        This method indicates that the sender wants to close the
        channel. This may be due to internal conditions (e.g. a forced
        shut-down) or due to an error handling a specific method, i.e.
        an exception. When a close is due to an exception, the sender
        provides the class and method id of the method which caused
        the exception.

        RULE:

        > After sending this method any received method except
        > Channel.Close-OK MUST be discarded.

        RULE:

        > The peer sending this method MAY use a counter or timeout
        > to detect failure of the other peer to respond correctly
        > with Channel.Close-OK..

        PARAMETERS:
        :   reply\_code: short

            > The reply code. The AMQ reply codes are defined in AMQ
            > RFC 011.

            reply\_text: shortstr

            > The localised reply text. This text can be logged as an
            > aid to resolving issues.

            class\_id: short

            > failing method class
            >
            > When the close is provoked by a method exception, this
            > is the class of the method.

            method\_id: short

            > failing method ID
            >
            > When the close is provoked by a method exception, this
            > is the ID of the method.

    collect()[[source]](../_modules/amqp/channel.html#Channel.collect)
    :   Tear down this object.

        Best called after we’ve agreed to close with the server.

    confirm\_select(*nowait=False*)[[source]](../_modules/amqp/channel.html#Channel.confirm_select)
    :   Enable publisher confirms for this channel.

        Note: This is an RabbitMQ extension.

        Can now be used if the channel is in transactional mode.

        Parameters:
        :   **nowait** – If set, the server will not respond to the method.
            The client should not wait for a reply method. If the
            server could not complete the method it will raise a channel
            or connection exception.

    connection

    exchange\_bind(*destination*, *source=''*, *routing\_key=''*, *nowait=False*, *arguments=None*, *argsig='BsssbF'*)[[source]](../_modules/amqp/channel.html#Channel.exchange_bind)
    :   Bind an exchange to an exchange.

        RULE:

        > A server MUST allow and ignore duplicate bindings - that
        > is, two or more bind methods for a specific exchanges,
        > with identical arguments - without treating these as an
        > error.

        RULE:

        > A server MUST allow cycles of exchange bindings to be
        > created including allowing an exchange to be bound to
        > itself.

        RULE:

        > A server MUST not deliver the same message more than once
        > to a destination exchange, even if the topology of
        > exchanges and bindings results in multiple (even infinite)
        > routes to that exchange.

        PARAMETERS:
        :   reserved-1: short

            destination: shortstr

            > Specifies the name of the destination exchange to
            > bind.
            >
            > RULE:
            >
            > > A client MUST NOT be allowed to bind a non-
            > > existent destination exchange.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to
            > > mean the default exchange.

            source: shortstr

            > Specifies the name of the source exchange to bind.
            >
            > RULE:
            >
            > > A client MUST NOT be allowed to bind a non-
            > > existent source exchange.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to
            > > mean the default exchange.

            routing-key: shortstr

            > Specifies the routing key for the binding. The routing
            > key is used for routing messages depending on the
            > exchange configuration. Not all exchanges use a
            > routing key - refer to the specific exchange
            > documentation.

            no-wait: bit

            arguments: table

            > A set of arguments for the binding. The syntax and
            > semantics of these arguments depends on the exchange
            > class.

    exchange\_declare(*exchange*, *type*, *passive=False*, *durable=False*, *auto\_delete=True*, *nowait=False*, *arguments=None*, *argsig='BssbbbbbF'*)[[source]](../_modules/amqp/channel.html#Channel.exchange_declare)
    :   Declare exchange, create if needed.

        This method creates an exchange if it does not already exist,
        and if the exchange exists, verifies that it is of the correct
        and expected class.

        RULE:

        > The server SHOULD support a minimum of 16 exchanges per
        > virtual host and ideally, impose no limit except as
        > defined by available resources.

        PARAMETERS:
        :   exchange: shortstr

            > RULE:
            >
            > > Exchange names starting with “amq.” are reserved
            > > for predeclared and standardised exchanges. If
            > > the client attempts to create an exchange starting
            > > with “amq.”, the server MUST raise a channel
            > > exception with reply code 403 (access refused).

            type: shortstr

            > exchange type
            >
            > Each exchange belongs to one of a set of exchange
            > types implemented by the server. The exchange types
            > define the functionality of the exchange - i.e. how
            > messages are routed through it. It is not valid or
            > meaningful to attempt to change the type of an
            > existing exchange.
            >
            > RULE:
            >
            > > If the exchange already exists with a different
            > > type, the server MUST raise a connection exception
            > > with a reply code 507 (not allowed).
            >
            > RULE:
            >
            > > If the server does not support the requested
            > > exchange type it MUST raise a connection exception
            > > with a reply code 503 (command invalid).

            passive: boolean

            > do not create exchange
            >
            > If set, the server will not create the exchange. The
            > client can use this to check whether an exchange
            > exists without modifying the server state.
            >
            > RULE:
            >
            > > If set, and the exchange does not already exist,
            > > the server MUST raise a channel exception with
            > > reply code 404 (not found).

            durable: boolean

            > request a durable exchange
            >
            > If set when creating a new exchange, the exchange will
            > be marked as durable. Durable exchanges remain active
            > when a server restarts. Non-durable exchanges
            > (transient exchanges) are purged if/when a server
            > restarts.
            >
            > RULE:
            >
            > > The server MUST support both durable and transient
            > > exchanges.
            >
            > RULE:
            >
            > > The server MUST ignore the durable field if the
            > > exchange already exists.

            auto\_delete: boolean

            > auto-delete when unused
            >
            > If set, the exchange is deleted when all queues have
            > finished using it.
            >
            > RULE:
            >
            > > The server SHOULD allow for a reasonable delay
            > > between the point when it determines that an
            > > exchange is not being used (or no longer used),
            > > and the point when it deletes the exchange. At
            > > the least it must allow a client to create an
            > > exchange and then bind a queue to it, with a small
            > > but non-zero delay between these two actions.
            >
            > RULE:
            >
            > > The server MUST ignore the auto-delete field if
            > > the exchange already exists.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

            arguments: table

            > arguments for declaration
            >
            > A set of arguments for the declaration. The syntax and
            > semantics of these arguments depends on the server
            > implementation. This field is ignored if passive is
            > True.

    exchange\_delete(*exchange*, *if\_unused=False*, *nowait=False*, *argsig='Bsbb'*)[[source]](../_modules/amqp/channel.html#Channel.exchange_delete)
    :   Delete an exchange.

        This method deletes an exchange. When an exchange is deleted
        all queue bindings on the exchange are cancelled.

        PARAMETERS:
        :   exchange: shortstr

            > RULE:
            >
            > > The exchange MUST exist. Attempting to delete a
            > > non-existing exchange causes a channel exception.

            if\_unused: boolean

            > delete only if unused
            >
            > If set, the server will only delete the exchange if it
            > has no queue bindings. If the exchange has queue
            > bindings the server does not delete it but raises a
            > channel exception instead.
            >
            > RULE:
            >
            > > If set, the server SHOULD delete the exchange but
            > > only if it has no queue bindings.
            >
            > RULE:
            >
            > > If set, the server SHOULD raise a channel
            > > exception if the exchange is in use.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

    exchange\_unbind(*destination*, *source=''*, *routing\_key=''*, *nowait=False*, *arguments=None*, *argsig='BsssbF'*)[[source]](../_modules/amqp/channel.html#Channel.exchange_unbind)
    :   Unbind an exchange from an exchange.

        RULE:

        > If a unbind fails, the server MUST raise a connection
        > exception.

        PARAMETERS:
        :   reserved-1: short

            destination: shortstr

            > Specifies the name of the destination exchange to
            > unbind.
            >
            > RULE:
            >
            > > The client MUST NOT attempt to unbind an exchange
            > > that does not exist from an exchange.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to
            > > mean the default exchange.

            source: shortstr

            > Specifies the name of the source exchange to unbind.
            >
            > RULE:
            >
            > > The client MUST NOT attempt to unbind an exchange
            > > from an exchange that does not exist.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to
            > > mean the default exchange.

            routing-key: shortstr

            > Specifies the routing key of the binding to unbind.

            no-wait: bit

            arguments: table

            > Specifies the arguments of the binding to unbind.

    flow(*active*)[[source]](../_modules/amqp/channel.html#Channel.flow)
    :   Enable/disable flow from peer.

        This method asks the peer to pause or restart the flow of
        content data. This is a simple flow-control mechanism that a
        peer can use to avoid overflowing its queues or otherwise
        finding itself receiving more messages than it can process.
        Note that this method is not intended for window control. The
        peer that receives a request to stop sending content should
        finish sending the current content, if any, and then wait
        until it receives a Flow restart method.

        RULE:

        > When a new channel is opened, it is active. Some
        > applications assume that channels are inactive until
        > started. To emulate this behaviour a client MAY open the
        > channel, then pause it.

        RULE:

        > When sending content data in multiple frames, a peer
        > SHOULD monitor the channel for incoming methods and
        > respond to a Channel.Flow as rapidly as possible.

        RULE:

        > A peer MAY use the Channel.Flow method to throttle
        > incoming content data for internal reasons, for example,
        > when exchanging data over a slower connection.

        RULE:

        > The peer that requests a Channel.Flow method MAY
        > disconnect and/or ban a peer that does not respect the
        > request.

        PARAMETERS:
        :   active: boolean

            > start/stop content frames
            >
            > If True, the peer starts sending content frames. If
            > False, the peer stops sending content frames.

    is\_closing

    method\_queue

    open()[[source]](../_modules/amqp/channel.html#Channel.open)
    :   Open a channel for use.

        This method opens a virtual connection (a channel).

        RULE:

        > This method MUST NOT be called when the channel is already
        > open.

        PARAMETERS:
        :   out\_of\_band: shortstr (DEPRECATED)

            > out-of-band settings
            >
            > Configures out-of-band transfers on this channel. The
            > syntax and meaning of this field will be formally
            > defined at a later date.

    queue\_bind(*queue*, *exchange=''*, *routing\_key=''*, *nowait=False*, *arguments=None*, *argsig='BsssbF'*)[[source]](../_modules/amqp/channel.html#Channel.queue_bind)
    :   Bind queue to an exchange.

        This method binds a queue to an exchange. Until a queue is
        bound it will not receive any messages. In a classic
        messaging model, store-and-forward queues are bound to a dest
        exchange and subscription queues are bound to a dest\_wild
        exchange.

        RULE:

        > A server MUST allow ignore duplicate bindings - that is,
        > two or more bind methods for a specific queue, with
        > identical arguments - without treating these as an error.

        RULE:

        > If a bind fails, the server MUST raise a connection
        > exception.

        RULE:

        > The server MUST NOT allow a durable queue to bind to a
        > transient exchange. If the client attempts this the server
        > MUST raise a channel exception.

        RULE:

        > Bindings for durable queues are automatically durable and
        > the server SHOULD restore such bindings after a server
        > restart.

        RULE:

        > The server SHOULD support at least 4 bindings per queue,
        > and ideally, impose no limit except as defined by
        > available resources.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to bind. If the queue
            > name is empty, refers to the current queue for the
            > channel, which is the last declared queue.
            >
            > RULE:
            >
            > > If the client did not previously declare a queue,
            > > and the queue name in this method is empty, the
            > > server MUST raise a connection exception with
            > > reply code 530 (not allowed).
            >
            > RULE:
            >
            > > If the queue does not exist the server MUST raise
            > > a channel exception with reply code 404 (not
            > > found).

            exchange: shortstr

            > The name of the exchange to bind to.
            >
            > RULE:
            >
            > > If the exchange does not exist the server MUST
            > > raise a channel exception with reply code 404 (not
            > > found).

            routing\_key: shortstr

            > message routing key
            >
            > Specifies the routing key for the binding. The
            > routing key is used for routing messages depending on
            > the exchange configuration. Not all exchanges use a
            > routing key - refer to the specific exchange
            > documentation. If the routing key is empty and the
            > queue name is empty, the routing key will be the
            > current queue for the channel, which is the last
            > declared queue.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

            arguments: table

            > arguments for binding
            >
            > A set of arguments for the binding. The syntax and
            > semantics of these arguments depends on the exchange
            > class.

    queue\_declare(*queue=''*, *passive=False*, *durable=False*, *exclusive=False*, *auto\_delete=True*, *nowait=False*, *arguments=None*, *argsig='BsbbbbbF'*)[[source]](../_modules/amqp/channel.html#Channel.queue_declare)
    :   Declare queue, create if needed.

        This method creates or checks a queue. When creating a new
        queue the client can specify various properties that control
        the durability of the queue and its contents, and the level of
        sharing for the queue.

        RULE:

        > The server MUST create a default binding for a newly-
        > created queue to the default exchange, which is an
        > exchange of type ‘direct’.

        RULE:

        > The server SHOULD support a minimum of 256 queues per
        > virtual host and ideally, impose no limit except as
        > defined by available resources.

        PARAMETERS:
        :   queue: shortstr

            > RULE:
            >
            > > The queue name MAY be empty, in which case the
            > > server MUST create a new queue with a unique
            > > generated name and return this to the client in
            > > the Declare-Ok method.
            >
            > RULE:
            >
            > > Queue names starting with “amq.” are reserved for
            > > predeclared and standardised server queues. If
            > > the queue name starts with “amq.” and the passive
            > > option is False, the server MUST raise a connection
            > > exception with reply code 403 (access refused).

            passive: boolean

            > do not create queue
            >
            > If set, the server will not create the queue. The
            > client can use this to check whether a queue exists
            > without modifying the server state.
            >
            > RULE:
            >
            > > If set, and the queue does not already exist, the
            > > server MUST respond with a reply code 404 (not
            > > found) and raise a channel exception.

            durable: boolean

            > request a durable queue
            >
            > If set when creating a new queue, the queue will be
            > marked as durable. Durable queues remain active when
            > a server restarts. Non-durable queues (transient
            > queues) are purged if/when a server restarts. Note
            > that durable queues do not necessarily hold persistent
            > messages, although it does not make sense to send
            > persistent messages to a transient queue.
            >
            > RULE:
            >
            > > The server MUST recreate the durable queue after a
            > > restart.
            >
            > RULE:
            >
            > > The server MUST support both durable and transient
            > > queues.
            >
            > RULE:
            >
            > > The server MUST ignore the durable field if the
            > > queue already exists.

            exclusive: boolean

            > request an exclusive queue
            >
            > Exclusive queues may only be consumed from by the
            > current connection. Setting the ‘exclusive’ flag
            > always implies ‘auto-delete’.
            >
            > RULE:
            >
            > > The server MUST support both exclusive (private)
            > > and non-exclusive (shared) queues.
            >
            > RULE:
            >
            > > The server MUST raise a channel exception if
            > > ‘exclusive’ is specified and the queue already
            > > exists and is owned by a different connection.

            auto\_delete: boolean

            > auto-delete queue when unused
            >
            > If set, the queue is deleted when all consumers have
            > finished using it. Last consumer can be cancelled
            > either explicitly or because its channel is closed. If
            > there was no consumer ever on the queue, it won’t be
            > deleted.
            >
            > RULE:
            >
            > > The server SHOULD allow for a reasonable delay
            > > between the point when it determines that a queue
            > > is not being used (or no longer used), and the
            > > point when it deletes the queue. At the least it
            > > must allow a client to create a queue and then
            > > create a consumer to read from it, with a small
            > > but non-zero delay between these two actions. The
            > > server should equally allow for clients that may
            > > be disconnected prematurely, and wish to re-
            > > consume from the same queue without losing
            > > messages. We would recommend a configurable
            > > timeout, with a suitable default value being one
            > > minute.
            >
            > RULE:
            >
            > > The server MUST ignore the auto-delete field if
            > > the queue already exists.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

            arguments: table

            > arguments for declaration
            >
            > A set of arguments for the declaration. The syntax and
            > semantics of these arguments depends on the server
            > implementation. This field is ignored if passive is
            > True.

        Returns a tuple containing 3 items:
        :   the name of the queue (essential for automatically-named queues),
            message count and
            consumer count

    queue\_delete(*queue=''*, *if\_unused=False*, *if\_empty=False*, *nowait=False*, *argsig='Bsbbb'*)[[source]](../_modules/amqp/channel.html#Channel.queue_delete)
    :   Delete a queue.

        This method deletes a queue. When a queue is deleted any
        pending messages are sent to a dead-letter queue if this is
        defined in the server configuration, and all consumers on the
        queue are cancelled.

        RULE:

        > The server SHOULD use a dead-letter queue to hold messages
        > that were pending on a deleted queue, and MAY provide
        > facilities for a system administrator to move these
        > messages back to an active queue.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to delete. If the
            > queue name is empty, refers to the current queue for
            > the channel, which is the last declared queue.
            >
            > RULE:
            >
            > > If the client did not previously declare a queue,
            > > and the queue name in this method is empty, the
            > > server MUST raise a connection exception with
            > > reply code 530 (not allowed).
            >
            > RULE:
            >
            > > The queue must exist. Attempting to delete a non-
            > > existing queue causes a channel exception.

            if\_unused: boolean

            > delete only if unused
            >
            > If set, the server will only delete the queue if it
            > has no consumers. If the queue has consumers the
            > server does does not delete it but raises a channel
            > exception instead.
            >
            > RULE:
            >
            > > The server MUST respect the if-unused flag when
            > > deleting a queue.

            if\_empty: boolean

            > delete only if empty
            >
            > If set, the server will only delete the queue if it
            > has no messages. If the queue is not empty the server
            > raises a channel exception.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

        If nowait is False, returns the number of deleted messages.

    queue\_purge(*queue=''*, *nowait=False*, *argsig='Bsb'*)[[source]](../_modules/amqp/channel.html#Channel.queue_purge)
    :   Purge a queue.

        This method removes all messages from a queue. It does not
        cancel consumers. Purged messages are deleted without any
        formal “undo” mechanism.

        RULE:

        > A call to purge MUST result in an empty queue.

        RULE:

        > On transacted channels the server MUST not purge messages
        > that have already been sent to a client but not yet
        > acknowledged.

        RULE:

        > The server MAY implement a purge queue or log that allows
        > system administrators to recover accidentally-purged
        > messages. The server SHOULD NOT keep purged messages in
        > the same storage spaces as the live messages since the
        > volumes of purged messages may get very large.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to purge. If the
            > queue name is empty, refers to the current queue for
            > the channel, which is the last declared queue.
            >
            > RULE:
            >
            > > If the client did not previously declare a queue,
            > > and the queue name in this method is empty, the
            > > server MUST raise a connection exception with
            > > reply code 530 (not allowed).
            >
            > RULE:
            >
            > > The queue must exist. Attempting to purge a non-
            > > existing queue causes a channel exception.

            nowait: boolean

            > do not send a reply method
            >
            > If set, the server will not respond to the method. The
            > client should not wait for a reply method. If the
            > server could not complete the method it will raise a
            > channel or connection exception.

        If nowait is False, returns a number of purged messages.

    queue\_unbind(*queue*, *exchange*, *routing\_key=''*, *nowait=False*, *arguments=None*, *argsig='BsssF'*)[[source]](../_modules/amqp/channel.html#Channel.queue_unbind)
    :   Unbind a queue from an exchange.

        This method unbinds a queue from an exchange.

        RULE:

        > If a unbind fails, the server MUST raise a connection exception.

        PARAMETERS:
        :   queue: shortstr

            > Specifies the name of the queue to unbind.
            >
            > RULE:
            >
            > > The client MUST either specify a queue name or have
            > > previously declared a queue on the same channel
            >
            > RULE:
            >
            > > The client MUST NOT attempt to unbind a queue that
            > > does not exist.

            exchange: shortstr

            > The name of the exchange to unbind from.
            >
            > RULE:
            >
            > > The client MUST NOT attempt to unbind a queue from an
            > > exchange that does not exist.
            >
            > RULE:
            >
            > > The server MUST accept a blank exchange name to mean
            > > the default exchange.

            routing\_key: shortstr

            > routing key of binding
            >
            > Specifies the routing key of the binding to unbind.

            arguments: table

            > arguments of binding
            >
            > Specifies the arguments of the binding to unbind.

    then(*on\_success*, *on\_error=None*)[[source]](../_modules/amqp/channel.html#Channel.then)

    tx\_commit()[[source]](../_modules/amqp/channel.html#Channel.tx_commit)
    :   Commit the current transaction.

        This method commits all messages published and acknowledged in
        the current transaction. A new transaction starts immediately
        after a commit.

    tx\_rollback()[[source]](../_modules/amqp/channel.html#Channel.tx_rollback)
    :   Abandon the current transaction.

        This method abandons all messages published and acknowledged
        in the current transaction. A new transaction starts
        immediately after a rollback.

    tx\_select()[[source]](../_modules/amqp/channel.html#Channel.tx_select)
    :   Select standard transaction mode.

        This method sets the channel to use standard transactions.
        The client must use this method at least once on a channel
        before using the Commit or Rollback methods.