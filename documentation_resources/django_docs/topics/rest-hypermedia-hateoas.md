<!-- Source: https://www.django-rest-framework.org/topics/rest-hypermedia-hateoas -->

# REST, Hypermedia & HATEOAS

> You keep using that word "REST". I do not think it means what you think it means.
>
> — Mike Amundsen, [REST fest 2012 keynote](https://vimeo.com/channels/restfest/49503453).

First off, the disclaimer. The name "Django REST framework" was decided back in early 2011 and was chosen simply to ensure the project would be easily found by developers. Throughout the documentation we try to use the more simple and technically correct terminology of "Web APIs".

If you are serious about designing a Hypermedia API, you should look to resources outside of this documentation to help inform your design choices.

The following fall into the "required reading" category.

- Roy Fielding's dissertation - [Architectural Styles and
  the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).
- Roy Fielding's "[REST APIs must be hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)" blog post.
- Leonard Richardson & Mike Amundsen's [RESTful Web APIs](http://restfulwebapis.org/).
- Mike Amundsen's [Building Hypermedia APIs with HTML5 and Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578).
- Steve Klabnik's [Designing Hypermedia APIs](http://designinghypermediaapis.com/).
- The [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html).

For a more thorough background, check out Klabnik's [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list).

## Building Hypermedia APIs with REST framework

REST framework is an agnostic Web API toolkit. It does help guide you towards building well-connected APIs, and makes it easy to design appropriate media types, but it does not strictly enforce any particular design style.

## What REST framework provides.

It is self evident that REST framework makes it possible to build Hypermedia APIs. The browsable API that it offers is built on HTML - the hypermedia language of the web.

REST framework also includes [serialization](../../api-guide/serializers/) and [parser](../../api-guide/parsers/)/[renderer](../../api-guide/renderers/) components that make it easy to build appropriate media types, [hyperlinked relations](../../api-guide/fields/) for building well-connected systems, and great support for [content negotiation](../../api-guide/content-negotiation/).

## What REST framework doesn't provide.

What REST framework doesn't do is give you machine readable hypermedia formats such as [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) or HTML [microformats](http://microformats.org/wiki/Main_Page) by default, or the ability to auto-magically create fully HATEOAS style APIs that include hypermedia-based form descriptions and semantically labeled hyperlinks. Doing so would involve making opinionated choices about API design that should really remain outside of the framework's scope.

Back to top