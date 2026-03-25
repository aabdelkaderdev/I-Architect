<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.rpc.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.rpc.html).

# `celery.backends.rpc`

The `RPC` result backend for AMQP brokers.

RPC-style result backend, using reply-to and one queue per client.

exception celery.backends.rpc.BacklogLimitExceeded[[source]](../../_modules/celery/backends/rpc.html#BacklogLimitExceeded)
:   Too much state history to fast-forward.

class celery.backends.rpc.RPCBackend(*app*, *connection=None*, *exchange=None*, *exchange\_type=None*, *persistent=None*, *serializer=None*, *auto\_delete=True*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend)
:   Base class for the RPC result backend.

    exception BacklogLimitExceeded
    :   Exception raised when there are too many messages for a task id.

    class Consumer(*channel*, *queues=None*, *no\_ack=None*, *auto\_declare=None*, *callbacks=None*, *on\_decode\_error=None*, *on\_message=None*, *accept=None*, *prefetch\_count=None*, *tag\_prefix=None*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.Consumer)
    :   Consumer that requires manual declaration of queues.

        auto\_declare = False
        :   By default all entities will be declared at instantiation, if you
            want to handle this manually you can set this to `False`.

    class Exchange(*name=''*, *type=''*, *channel=None*, *\*\*kwargs*)
    :   An Exchange declaration.

        ## Arguments:

        > name (str): See [`name`](#id0 "celery.backends.rpc.RPCBackend.Exchange.name").
        > type (str): See [`type`](#id5 "celery.backends.rpc.RPCBackend.Exchange.type").
        > channel (kombu.Connection, ChannelT): See `channel`.
        > durable (bool): See [`durable`](#celery.backends.rpc.RPCBackend.Exchange.durable "celery.backends.rpc.RPCBackend.Exchange.durable").
        > auto\_delete (bool): See [`auto_delete`](#celery.backends.rpc.RPCBackend.Exchange.auto_delete "celery.backends.rpc.RPCBackend.Exchange.auto_delete").
        > delivery\_mode (enum): See [`delivery_mode`](#celery.backends.rpc.RPCBackend.Exchange.delivery_mode "celery.backends.rpc.RPCBackend.Exchange.delivery_mode").
        > arguments (Dict): See `arguments`.
        > no\_declare (bool): See [`no_declare`](#celery.backends.rpc.RPCBackend.Exchange.no_declare "celery.backends.rpc.RPCBackend.Exchange.no_declare")

        name(*str*)
        :   Default is no name (the default exchange).

            Type:
            :   Name of the exchange.

        type(*str*)
        :   *This description of AMQP exchange types was shamelessly stolen
            from the blog post `AMQP in 10 minutes: Part 4`\_ by
            Rajith Attapattu. Reading this article is recommended if you’re
            new to amqp.*

            “AMQP defines four default exchange types (routing algorithms) that
            covers most of the common messaging use cases. An AMQP broker can
            also define additional exchange types, so see your broker
            manual for more information about available exchange types.

            > > - direct (*default*)
            > >
            > >   > Direct match between the routing key in the message,
            > >   > and the routing criteria used when a queue is bound to
            > >   > this exchange.
            > > - topic
            > >
            > >   > Wildcard match between the routing key and the routing
            > >   > pattern specified in the exchange/queue binding.
            > >   > The routing key is treated as zero or more words delimited
            > >   > by “.” and supports special wildcard characters. “\*”
            > >   > matches a single word and “#” matches zero or more words.
            > > - fanout
            > >
            > >   > Queues are bound to this exchange with no arguments. Hence
            > >   > any message sent to this exchange will be forwarded to all
            > >   > queues bound to this exchange.
            > > - headers
            > >
            > >   > Queues are bound to this exchange with a table of arguments
            > >   > containing headers and values (optional). A special
            > >   > argument named “x-match” determines the matching algorithm,
            > >   > where “all” implies an AND (all pairs must match) and
            > >   > “any” implies OR (at least one pair must match).
            > >   >
            > >   > `arguments` is used to specify the arguments.
            >
            > channel (ChannelT): The channel the exchange is bound to (if bound).
            >
            > durable (bool): Durable exchanges remain active when a server restarts.
            > :   Non-durable exchanges (transient exchanges) are purged when a
            >     server restarts. Default is `True`.
            >
            > auto\_delete (bool): If set, the exchange is deleted when all queues
            > :   have finished using it. Default is `False`.
            >
            > delivery\_mode (enum): The default delivery mode used for messages.
            > :   The value is an integer, or alias string.
            >
            >     > - 1 or “transient”
            >     >
            >     >   > The message is transient. Which means it is stored in
            >     >   > memory only, and is lost if the server dies or restarts.
            >     > - 2 or “persistent” (*default*)
            >     >   :   The message is persistent. Which means the message is
            >     >       stored both in-memory, and on disk, and therefore
            >     >       preserved if the server dies or restarts.
            >
            >     The default value is 2 (persistent).
            >
            > arguments (Dict): Additional arguments to specify when the exchange
            > :   is declared.
            >
            > no\_declare (bool): Never declare this exchange
            > :   ([`declare()`](#celery.backends.rpc.RPCBackend.Exchange.declare "celery.backends.rpc.RPCBackend.Exchange.declare") does nothing).

        Message(*body*, *delivery\_mode=None*, *properties=None*, *\*\*kwargs*)
        :   Create message instance to be sent with [`publish()`](#celery.backends.rpc.RPCBackend.Exchange.publish "celery.backends.rpc.RPCBackend.Exchange.publish").

            ### Arguments:

            > body (Any): Message body.
            >
            > delivery\_mode (bool): Set custom delivery mode.
            > :   Defaults to [`delivery_mode`](#celery.backends.rpc.RPCBackend.Exchange.delivery_mode "celery.backends.rpc.RPCBackend.Exchange.delivery_mode").
            >
            > priority (int): Message priority, 0 to broker configured
            > :   max priority, where higher is better.
            >
            > content\_type (str): The messages content\_type. If content\_type
            > :   is set, no serialization occurs as it is assumed this is either
            >     a binary object, or you’ve done your own serialization.
            >     Leave blank if using built-in serialization as our library
            >     properly sets content\_type.
            >
            > content\_encoding (str): The character set in which this object
            > :   is encoded. Use “binary” if sending in raw binary objects.
            >     Leave blank if using built-in serialization as our library
            >     properly sets content\_encoding.
            >
            > properties (Dict): Message properties.
            >
            > headers (Dict): Message headers.

        PERSISTENT\_DELIVERY\_MODE = 2

        TRANSIENT\_DELIVERY\_MODE = 1

        attrs: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), Any], ...] = (('name', None), ('type', None), ('arguments', None), ('durable', <class 'bool'>), ('passive', <class 'bool'>), ('auto\_delete', <class 'bool'>), ('delivery\_mode', <function Exchange.<lambda>>), ('no\_declare', <class 'bool'>))

        auto\_delete = False

        bind\_to(*exchange=''*, *routing\_key=''*, *arguments=None*, *nowait=False*, *channel=None*, *\*\*kwargs*)
        :   Bind the exchange to another exchange.

            ### Arguments:

            > nowait (bool): If set the server will not respond, and the call
            > :   will not block waiting for a response.
            >     Default is `False`.

        binding(*routing\_key=''*, *arguments=None*, *unbind\_arguments=None*)

        property can\_cache\_declaration
        :   bool(x) -> bool

            Returns True when the argument x is true, False otherwise.
            The builtins True and False are the only two instances of the class bool.
            The class bool is a subclass of the class int, and cannot be subclassed.

        declare(*nowait=False*, *passive=None*, *channel=None*)
        :   Declare the exchange.

            Creates the exchange on the broker, unless passive is set
            in which case it will only assert that the exchange exists.

            Argument:
            :   nowait (bool): If set the server will not respond, and a
                :   response will not be waited for. Default is `False`.

        delete(*if\_unused=False*, *nowait=False*)
        :   Delete the exchange declaration on server.

            ### Arguments:

            > if\_unused (bool): Delete only if the exchange has no bindings.
            > :   Default is `False`.
            >
            > nowait (bool): If set the server will not respond, and a
            > :   response will not be waited for. Default is `False`.

        delivery\_mode = None

        durable = True

        name = ''

        no\_declare = False

        passive = False

        publish(*message*, *routing\_key=None*, *mandatory=False*, *immediate=False*, *exchange=None*)
        :   Publish message.

            ### Arguments:

            > message (Union[kombu.Message, str, bytes]):
            > :   Message to publish.
            >
            > routing\_key (str): Message routing key.
            > mandatory (bool): Currently not supported.
            > immediate (bool): Currently not supported.

        type = 'direct'

        unbind\_from(*source=''*, *routing\_key=''*, *nowait=False*, *arguments=None*, *channel=None*)
        :   Delete previously created exchange binding from the server.

    class Producer(*channel*, *exchange=None*, *routing\_key=None*, *serializer=None*, *auto\_declare=None*, *compression=None*, *on\_return=None*)
    :   Message Producer.

        ## Arguments:

        > channel (kombu.Connection, ChannelT): Connection or channel.
        > exchange (kombu.entity.Exchange, str): Optional default exchange.
        > routing\_key (str): Optional default routing key.
        > serializer (str): Default serializer. Default is “json”.
        > compression (str): Default compression method.
        >
        > > Default is no compression.
        >
        > auto\_declare (bool): Automatically declare the default exchange
        > :   at instantiation. Default is `True`.
        >
        > on\_return (Callable): Callback to call for undeliverable messages,
        > :   when the mandatory or immediate arguments to
        >     [`publish()`](#celery.backends.rpc.RPCBackend.Producer.publish "celery.backends.rpc.RPCBackend.Producer.publish") is used. This callback needs the following
        >     signature: (exception, exchange, routing\_key, message).
        >     Note that the producer needs to drain events to use this feature.

        auto\_declare = True
        :   By default, if a default exchange is set,
            that exchange will be declare when publishing a message.

        property channel

        close()

        compression = None
        :   Default compression method. Disabled by default.

        property connection

        declare()
        :   Declare the exchange.

            ### Note:

            > This happens automatically at instantiation when
            > the [`auto_declare`](#celery.backends.rpc.RPCBackend.Producer.auto_declare "celery.backends.rpc.RPCBackend.Producer.auto_declare") flag is enabled.

        exchange = None
        :   Default exchange

        maybe\_declare(*entity*, *retry=False*, *\*\*retry\_policy*)
        :   Declare exchange if not already declared during this session.

        on\_return = None
        :   Basic return callback.

        publish(*body*, *routing\_key=None*, *delivery\_mode=None*, *mandatory=False*, *immediate=False*, *priority=0*, *content\_type=None*, *content\_encoding=None*, *serializer=None*, *headers=None*, *compression=None*, *exchange=None*, *retry=False*, *retry\_policy=None*, *declare=None*, *expiration=None*, *timeout=None*, *confirm\_timeout=None*, *\*\*properties*)
        :   Publish message to the specified exchange.

            ### Arguments:

            > body (Any): Message body.
            > routing\_key (str): Message routing key.
            > delivery\_mode (enum): See `delivery_mode`.
            > mandatory (bool): Currently not supported.
            > immediate (bool): Currently not supported.
            > priority (int): Message priority. A number between 0 and 9.
            > content\_type (str): Content type. Default is auto-detect.
            > content\_encoding (str): Content encoding. Default is auto-detect.
            > serializer (str): Serializer to use. Default is auto-detect.
            > compression (str): Compression method to use. Default is none.
            > headers (Dict): Mapping of arbitrary headers to pass along
            >
            > > with the message body.
            >
            > exchange (kombu.entity.Exchange, str): Override the exchange.
            > :   Note that this exchange must have been declared.
            >
            > declare (Sequence[EntityT]): Optional list of required entities
            > :   that must have been declared before publishing the message.
            >     The entities will be declared using
            >     [`maybe_declare()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.common.html#kombu.common.maybe_declare "(in Kombu v5.6)").
            >
            > retry (bool): Retry publishing, or declaring entities if the
            > :   connection is lost.
            >
            > retry\_policy (Dict): Retry configuration, this is the keywords
            > :   supported by [`ensure()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection.ensure "(in Kombu v5.6)").
            >
            > expiration (float): A TTL in seconds can be specified per message.
            > :   Default is no expiration.
            >
            > timeout (float): Set timeout to wait maximum timeout second
            > :   for message to publish.
            >
            > confirm\_timeout (float): Set confirm timeout to wait maximum timeout second
            > :   for message to confirm publishing if the channel is set to confirm publish mode.
            >
            > [\*\*](#id8)properties (Any): Additional message properties, see AMQP spec.

        release()

        revive(*channel*)
        :   Revive the producer after connection loss.

        routing\_key = ''
        :   Default routing key.

        serializer = None
        :   Default serializer to use. Default is JSON.

    class Queue(*name=''*, *exchange=None*, *routing\_key=''*, *channel=None*, *bindings=None*, *on\_declared=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.Queue)
    :   Queue that never caches declaration.

        can\_cache\_declaration = False
        :   Defines whether maybe\_declare can skip declaring this entity twice.

    class ResultConsumer(*\*args*, *\*\*kwargs*)
    :   class Consumer(*channel*, *queues=None*, *no\_ack=None*, *auto\_declare=None*, *callbacks=None*, *on\_decode\_error=None*, *on\_message=None*, *accept=None*, *prefetch\_count=None*, *tag\_prefix=None*)
        :   Message consumer.

            ## Arguments:

            > channel (kombu.Connection, ChannelT): see [`channel`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.channel "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.channel").
            > queues (Sequence[kombu.Queue]): see [`queues`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.queues "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.queues").
            > no\_ack (bool): see [`no_ack`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack").
            > auto\_declare (bool): see [`auto_declare`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.auto_declare "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.auto_declare")
            > callbacks (Sequence[Callable]): see [`callbacks`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks").
            > on\_message (Callable): See [`on_message`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.on_message "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.on_message")
            > on\_decode\_error (Callable): see [`on_decode_error`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.on_decode_error "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.on_decode_error").
            > prefetch\_count (int): see [`prefetch_count`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.prefetch_count "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.prefetch_count").

            exception ContentDisallowed
            :   Consumer does not allow this content-type.

            accept = None
            :   List of accepted content-types.

                An exception will be raised if the consumer receives
                a message with an untrusted content type.
                By default all content-types are accepted, but not if
                `kombu.disable_untrusted_serializers()` was called,
                in which case only json is allowed.

            add\_queue(*queue*)
            :   Add a queue to the list of queues to consume from.

                ### Note:

                > This will not start consuming from the queue,
                > for that you will have to call [`consume()`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.consume "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.consume") after.

            auto\_declare = True
            :   By default all entities will be declared at instantiation, if you
                want to handle this manually you can set this to `False`.

            callbacks = None
            :   List of callbacks called in order when a message is received.

                The signature of the callbacks must take two arguments:
                (body, message), which is the decoded message body and
                the `Message` instance.

            cancel()
            :   End all active queue consumers.

                ### Note:

                > This does not affect already delivered messages, but it does
                > mean the server will not send any more messages for this consumer.

            cancel\_by\_queue(*queue*)
            :   Cancel consumer by queue name.

            channel = None
            :   The connection/channel to use for this consumer.

            close()
            :   End all active queue consumers.

                ### Note:

                > This does not affect already delivered messages, but it does
                > mean the server will not send any more messages for this consumer.

            property connection

            consume(*no\_ack=None*)
            :   Start consuming messages.

                Can be called multiple times, but note that while it
                will consume from new queues added since the last call,
                it will not cancel consuming from removed queues (
                use [`cancel_by_queue()`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.cancel_by_queue "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.cancel_by_queue")).

                ### Arguments:

                > no\_ack (bool): See [`no_ack`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack").

            consuming\_from(*queue*)
            :   Return `True` if currently consuming from queue’.

            declare()
            :   Declare queues, exchanges and bindings.

                ### Note:

                > This is done automatically at instantiation
                > when [`auto_declare`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.auto_declare "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.auto_declare") is set.

            flow(*active*)
            :   Enable/disable flow from peer.

                This is a simple flow-control mechanism that a peer can use
                to avoid overflowing its queues or otherwise finding itself
                receiving more messages than it can process.

                The peer that receives a request to stop sending content
                will finish sending the current content (if any), and then wait
                until flow is reactivated.

            no\_ack = None
            :   Flag for automatic message acknowledgment.
                If enabled the messages are automatically acknowledged by the
                broker. This can increase performance but means that you
                have no control of when the message is removed.

                Disabled by default.

            on\_decode\_error = None
            :   Callback called when a message can’t be decoded.

                The signature of the callback must take two arguments: (message,
                exc), which is the message that can’t be decoded and the exception
                that occurred while trying to decode it.

            on\_message = None
            :   Optional function called whenever a message is received.

                When defined this function will be called instead of the
                [`receive()`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.receive "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.receive") method, and [`callbacks`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks") will be disabled.

                So this can be used as an alternative to [`callbacks`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks") when
                you don’t want the body to be automatically decoded.
                Note that the message will still be decompressed if the message
                has the `compression` header set.

                The signature of the callback must take a single argument,
                which is the `Message` object.

                Also note that the `message.body` attribute, which is the raw
                contents of the message body, may in some cases be a read-only
                `buffer` object.

            prefetch\_count = None
            :   Initial prefetch count

                If set, the consumer will set the prefetch\_count QoS value at startup.
                Can also be changed using [`qos()`](../../userguide/extending.html#qos "qos").

            purge()
            :   Purge messages from all queues.

                ### Warning:

                > This will *delete all ready messages*, there is no undo operation.

            qos(*prefetch\_size=0*, *prefetch\_count=0*, *apply\_global=False*)
            :   Specify quality of service.

                The client can request that messages should be sent in
                advance so that when the client finishes processing a message,
                the following message is already held locally, rather than needing
                to be sent down the channel. Prefetching gives a performance
                improvement.

                The prefetch window is Ignored if the [`no_ack`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.no_ack") option is set.

                ### Arguments:

                > prefetch\_size (int): Specify the prefetch window in octets.
                > :   The server will send a message in advance if it is equal to
                >     or smaller in size than the available prefetch size (and
                >     also falls within other prefetch limits). May be set to zero,
                >     meaning “no specific limit”, although other prefetch limits
                >     may still apply.
                >
                > prefetch\_count (int): Specify the prefetch window in terms of
                > :   whole messages.
                >
                > apply\_global (bool): Apply new settings globally on all channels.

            property queues

            receive(*body*, *message*)
            :   Method called when a message is received.

                This dispatches to the registered [`callbacks`](#celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks "celery.backends.rpc.RPCBackend.ResultConsumer.Consumer.callbacks").

                ### Arguments:

                > body (Any): The decoded message body.
                > message (~kombu.Message): The message instance.

                raises NotImplementedError:
                :   If no consumer callbacks have been: registered.

            recover(*requeue=False*)
            :   Redeliver unacknowledged messages.

                Asks the broker to redeliver all unacknowledged messages
                on the specified channel.

                ### Arguments:

                > requeue (bool): By default the messages will be redelivered
                > :   to the original recipient. With requeue set to true, the
                >     server will attempt to requeue the message, potentially then
                >     delivering it to an alternative subscriber.

            register\_callback(*callback*)
            :   Register a new callback to be called when a message is received.

                ### Note:

                > The signature of the callback needs to accept two arguments:
                > (body, message), which is the decoded message body
                > and the `Message` instance.

            revive(*channel*)
            :   Revive consumer after connection loss.

        cancel\_for(*task\_id*)

        consume\_from(*task\_id*)

        drain\_events(*timeout=None*)

        on\_after\_fork()

        start(*initial\_task\_id*, *no\_ack=True*, *\*\*kwargs*)

        stop()

    as\_uri(*include\_password=True*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.as_uri)
    :   Return the backend as an URI, sanitizing the password or not.

    property binding

    delete\_group(*group\_id*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.delete_group)

    destination\_for(*task\_id*, *request*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.destination_for)
    :   Get the destination for result by task id.

        Returns:
        :   tuple of `(reply_to, correlation_id)`.

        Return type:
        :   Tuple[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]

    ensure\_chords\_allowed()[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.ensure_chords_allowed)

    get\_task\_meta(*task\_id*, *backlog\_limit=1000*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.get_task_meta)
    :   Get task meta from backend.

        if always\_retry\_backend\_operation is activated, in the event of a recoverable exception,
        then retry operation with an exponential backoff until a limit has been reached.

    property oid

    on\_out\_of\_band\_result(*task\_id*, *message*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.on_out_of_band_result)

    on\_reply\_declare(*task\_id*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.on_reply_declare)

    on\_result\_fulfilled(*result*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.on_result_fulfilled)

    on\_task\_call(*producer*, *task\_id*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.on_task_call)

    persistent = False
    :   Set to true if the backend is persistent by default.

    poll(*task\_id*, *backlog\_limit=1000*)
    :   Get task meta from backend.

        if always\_retry\_backend\_operation is activated, in the event of a recoverable exception,
        then retry operation with an exponential backoff until a limit has been reached.

    reload\_group\_result(*task\_id*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.reload_group_result)
    :   Reload group result, even if it has been previously fetched.

    reload\_task\_result(*task\_id*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.reload_task_result)
    :   Reload task result, even if it has been previously fetched.

    restore\_group(*group\_id*, *cache=True*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.restore_group)
    :   Get the result for a group.

    retry\_policy = {'interval\_max': 1, 'interval\_start': 0, 'interval\_step': 1, 'max\_retries': 20}

    revive(*channel*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.revive)

    save\_group(*group\_id*, *result*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.save_group)
    :   Store the result of an executed group.

    store\_result(*task\_id*, *result*, *state*, *traceback=None*, *request=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/rpc.html#RPCBackend.store_result)
    :   Send task return value and state.

    supports\_autoexpire = True
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    supports\_native\_join = True
    :   If true the backend must implement `get_many()`.