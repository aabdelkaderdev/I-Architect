<!-- Source: https://docs.celeryq.dev/projects/amqp/en/latest/reference/amqp.exceptions.html -->

This document is for py-amqp's development version, which can be
significantly different from previous releases. Get the stable docs here:
[5.3](https://amqp.readthedocs.io/en/latest/reference/amqp.exceptions.html).

# `amqp.exceptions`

Exceptions used by amqp.

exception amqp.exceptions.AMQPDeprecationWarning[[source]](../_modules/amqp/exceptions.html#AMQPDeprecationWarning)
:   Warning for deprecated things.

exception amqp.exceptions.AMQPError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#AMQPError)
:   Base class for all AMQP exceptions.

    code = 0

    property method

exception amqp.exceptions.AMQPNotImplementedError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#AMQPNotImplementedError)
:   AMQP Not Implemented Error.

    code = 540

exception amqp.exceptions.AccessRefused(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#AccessRefused)
:   AMQP Access Refused Error.

    code = 403

exception amqp.exceptions.ChannelError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ChannelError)
:   AMQP Channel Error.

exception amqp.exceptions.ChannelNotOpen(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ChannelNotOpen)
:   AMQP Channel Not Open Error.

    code = 504

exception amqp.exceptions.ConnectionError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ConnectionError)
:   AMQP Connection Error.

exception amqp.exceptions.ConnectionForced(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ConnectionForced)
:   AMQP Connection Forced Error.

    code = 320

exception amqp.exceptions.ConsumerCancelled(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ConsumerCancelled)
:   AMQP Consumer Cancelled Predicate.

exception amqp.exceptions.ContentTooLarge(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ContentTooLarge)
:   AMQP Content Too Large Error.

    code = 311

exception amqp.exceptions.FrameError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#FrameError)
:   AMQP Frame Error.

    code = 501

exception amqp.exceptions.FrameSyntaxError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#FrameSyntaxError)
:   AMQP Frame Syntax Error.

    code = 502

exception amqp.exceptions.InternalError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#InternalError)
:   AMQP Internal Error.

    code = 541

exception amqp.exceptions.InvalidCommand(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#InvalidCommand)
:   AMQP Invalid Command Error.

    code = 503

exception amqp.exceptions.InvalidPath(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#InvalidPath)
:   AMQP Invalid Path Error.

    code = 402

exception amqp.exceptions.IrrecoverableChannelError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#IrrecoverableChannelError)
:   Exception class for irrecoverable channel errors.

exception amqp.exceptions.IrrecoverableConnectionError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#IrrecoverableConnectionError)
:   Exception class for irrecoverable connection errors.

exception amqp.exceptions.MessageNacked[[source]](../_modules/amqp/exceptions.html#MessageNacked)
:   Message was nacked by broker.

exception amqp.exceptions.NoConsumers(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#NoConsumers)
:   AMQP No Consumers Error.

    code = 313

exception amqp.exceptions.NotAllowed(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#NotAllowed)
:   AMQP Not Allowed Error.

    code = 530

exception amqp.exceptions.NotFound(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#NotFound)
:   AMQP Not Found Error.

    code = 404

exception amqp.exceptions.PreconditionFailed(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#PreconditionFailed)
:   AMQP Precondition Failed Error.

    code = 406

exception amqp.exceptions.RecoverableChannelError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#RecoverableChannelError)
:   Exception class for recoverable channel errors.

exception amqp.exceptions.RecoverableConnectionError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#RecoverableConnectionError)
:   Exception class for recoverable connection errors.

exception amqp.exceptions.ResourceError(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ResourceError)
:   AMQP Resource Error.

    code = 506

exception amqp.exceptions.ResourceLocked(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#ResourceLocked)
:   AMQP Resource Locked Error.

    code = 405

exception amqp.exceptions.UnexpectedFrame(*reply\_text=None*, *method\_sig=None*, *method\_name=None*, *reply\_code=None*)[[source]](../_modules/amqp/exceptions.html#UnexpectedFrame)
:   AMQP Unexpected Frame.

    code = 505