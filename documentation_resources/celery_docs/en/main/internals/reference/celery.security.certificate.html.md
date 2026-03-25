<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.security.certificate.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.certificate.html).

# `celery.security.certificate`

X.509 certificates.

class celery.security.certificate.CertStore[[source]](../../_modules/celery/security/certificate.html#CertStore)
:   Base class for certificate stores.

    add\_cert(*cert: [Certificate](#celery.security.certificate.Certificate "celery.security.certificate.Certificate")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#CertStore.add_cert)

    itercerts() → [Iterator](https://docs.python.org/dev/library/typing.html#typing.Iterator "(in Python v3.15)")[[Certificate](#celery.security.certificate.Certificate "celery.security.certificate.Certificate")][[source]](../../_modules/celery/security/certificate.html#CertStore.itercerts)
    :   Return certificate iterator.

class celery.security.certificate.Certificate(*cert: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*)[[source]](../../_modules/celery/security/certificate.html#Certificate)
:   X.509 certificate.

    get\_id() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#Certificate.get_id)
    :   Serial number/issuer pair uniquely identifies a certificate.

    get\_issuer() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#Certificate.get_issuer)
    :   Return issuer (CA) as a string.

    get\_pubkey() → DSAPublicKey | EllipticCurvePublicKey | Ed448PublicKey | Ed25519PublicKey | RSAPublicKey[[source]](../../_modules/celery/security/certificate.html#Certificate.get_pubkey)

    get\_serial\_number() → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#Certificate.get_serial_number)
    :   Return the serial number in the certificate.

    has\_expired() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#Certificate.has_expired)
    :   Check if the certificate has expired.

    verify(*data: [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")*, *signature: [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")*, *digest: HashAlgorithm | Prehashed*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/security/certificate.html#Certificate.verify)
    :   Verify signature for string containing data.

class celery.security.certificate.FSCertStore(*path: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*)[[source]](../../_modules/celery/security/certificate.html#FSCertStore)
:   File system certificate store.