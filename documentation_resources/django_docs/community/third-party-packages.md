<!-- Source: https://www.django-rest-framework.org/community/third-party-packages -->

# Third Party Packages

> Software ecosystems […] establish a community that further accelerates the sharing of knowledge, content, issues, expertise and skills.
>
> — [Jan Bosch](http://www.software-ecosystems.com/Software_Ecosystems/Ecosystems.html).

## About Third Party Packages

Third Party Packages allow developers to share code that extends the functionality of Django REST framework, in order to support additional use-cases.

We **support**, **encourage** and **strongly favor** the creation of Third Party Packages to encapsulate new behavior rather than adding additional functionality directly to Django REST Framework.

We aim to make creating third party packages as easy as possible, whilst keeping a **simple** and **well maintained** core API. By promoting third party packages we ensure that the responsibility for a package remains with its author. If a package proves suitably popular it can always be considered for inclusion into the core REST framework.

If you have an idea for a new feature please consider how it may be packaged as a Third Party Package. We're always happy to discuss ideas on the [Mailing List](https://groups.google.com/forum/#!forum/django-rest-framework).

## Creating a Third Party Package

### Version compatibility

Sometimes, in order to ensure your code works on various different versions of Django, Python or third party libraries, you'll need to run slightly different code depending on the environment. Any code that branches in this way should be isolated into a `compat.py` module, and should provide a single common interface that the rest of the codebase can use.

Check out Django REST framework's [compat.py](https://github.com/encode/django-rest-framework/blob/main/rest_framework/compat.py) for an example.

### Once your package is available

Once your package is decently documented and available on PyPI, you might want share it with others that might find it useful.

#### Adding to the Django REST framework grid

We suggest adding your package to the [REST Framework](https://www.djangopackages.com/grids/g/django-rest-framework/) grid on Django Packages.

#### Adding to the Django REST framework docs

Create a [Pull Request](https://github.com/encode/django-rest-framework/compare) on GitHub, and we'll add a link to it from the main REST framework documentation. You can add your package under **Third party packages** of the API Guide section that best applies, like [Authentication](../../api-guide/authentication/) or [Permissions](../../api-guide/permissions/). You can also link your package under the [Third Party Packages](#existing-third-party-packages) section.

#### Announce on the discussion group.

You can also let others know about your package through the [discussion group](https://groups.google.com/forum/#!forum/django-rest-framework).

## Existing Third Party Packages

Django REST Framework has a growing community of developers, packages, and resources.

Check out a grid detailing all the packages and ecosystem around Django REST Framework at [Django Packages](https://www.djangopackages.com/grids/g/django-rest-framework/).

To submit new content, [create a pull request](https://github.com/encode/django-rest-framework/compare).

### Async Support

- [adrf](https://github.com/em1208/adrf) - Async support, provides async Views, ViewSets, and Serializers.

### Authentication

- [djangorestframework-digestauth](https://github.com/juanriaza/django-rest-framework-digestauth) - Provides Digest Access Authentication support.
- [django-oauth-toolkit](https://github.com/evonove/django-oauth-toolkit) - Provides OAuth 2.0 support.
- [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) - Provides JSON Web Token Authentication support.
- [hawkrest](https://github.com/kumar303/hawkrest) - Provides Hawk HTTP Authorization.
- [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) - Provides an easy to use HTTP Signature Authentication mechanism.
- [djoser](https://github.com/sunscrapers/djoser) - Provides a set of views to handle basic actions such as registration, login, logout, password reset and account activation.
- [DRF Auth Kit](https://github.com/huynguyengl99/drf-auth-kit) - Provides complete REST authentication with JWT cookies, social login, MFA, and user management. Features full type safety and automatic OpenAPI schema generation.
- [dj-rest-auth](https://github.com/iMerica/dj-rest-auth) - Provides a set of REST API endpoints for registration, authentication (including social media authentication), password reset, retrieve and update user details, etc.
- [drf-oidc-auth](https://github.com/ByteInternet/drf-oidc-auth) - Implements OpenID Connect token authentication for DRF.
- [drfpasswordless](https://github.com/aaronn/django-rest-framework-passwordless) - Adds (Medium, Square Cash inspired) passwordless logins and signups via email and mobile numbers.
- [django-rest-authemail](https://github.com/celiao/django-rest-authemail) - Provides a RESTful API for user signup and authentication using email addresses.
- [dango-pyoidc](https://github.com/makinacorpus/django_pyoidc) adds support for OpenID Connect (OIDC) authentication.

### Permissions

- [drf-any-permissions](https://github.com/kevin-brown/drf-any-permissions) - Provides alternative permission handling.
- [djangorestframework-composed-permissions](https://github.com/niwibe/djangorestframework-composed-permissions) - Provides a simple way to define complex permissions.
- [rest\_condition](https://github.com/caxap/rest_condition) - Another extension for building complex permissions in a simple and convenient way.
- [dry-rest-permissions](https://github.com/FJNR-inc/dry-rest-permissions) - Provides a simple way to define permissions for individual api actions.
- [drf-access-policy](https://github.com/rsinger86/drf-access-policy) - Declarative and flexible permissions inspired by AWS' IAM policies.
- [drf-psq](https://github.com/drf-psq/drf-psq) - An extension that gives support for having action-based **permission\_classes**, **serializer\_class**, and **queryset** dependent on permission-based rules.
- [axioms-drf-py](https://github.com/abhishektiwari/axioms-drf-py) - Supports authentication and claim-based fine-grained authorization (**scopes**, **roles**, **groups**, **permissions**, etc. including object-level checks) using JWT tokens issued by an OAuth2/OIDC Authorization Server.

### Serializers

- [django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) - Serializer class that supports using MongoDB as the storage layer for Django REST framework.
- [djangorestframework-gis](https://github.com/djangonauts/django-rest-framework-gis) - Geographic add-ons
- [django-pydantic-field](https://github.com/surenkov/django-pydantic-field) - Provides a way to use Pydantic models as schemas for Django's JSONField with full support for Pydantic v1 and v2, type safety and integration with Django REST Framework.
- [drf-pydantic](https://github.com/georgebv/drf-pydantic) - Use Pydantic with Django REST framework for data validation and (de)serialization.
- [djangorestframework-hstore](https://github.com/djangonauts/django-rest-framework-hstore) - Serializer class to support django-hstore DictionaryField model field and its schema-mode feature.
- [djangorestframework-jsonapi](https://github.com/django-json-api/django-rest-framework-json-api) - Provides a parser, renderer, serializers, and other tools to help build an API that is compliant with the jsonapi.org spec.
- [html-json-forms](https://github.com/wq/html-json-forms) - Provides an algorithm and serializer to process HTML JSON Form submissions per the (inactive) spec.
- [django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) -
  Enables black/whitelisting fields, and conditionally expanding child serializers on a per-view/request basis.
- [djangorestframework-queryfields](https://github.com/wimglenn/djangorestframework-queryfields) - Serializer mixin allowing clients to control which fields will be sent in the API response.
- [drf-flex-fields](https://github.com/rsinger86/drf-flex-fields) - Serializer providing dynamic field expansion and sparse field sets via URL parameters.
- [drf-action-serializer](https://github.com/gregschmit/drf-action-serializer) - Serializer providing per-action fields config for use with ViewSets to prevent having to write multiple serializers.
- [djangorestframework-dataclasses](https://github.com/oxan/djangorestframework-dataclasses) - Serializer providing automatic field generation for Python dataclasses, like the built-in ModelSerializer does for models.
- [django-restql](https://github.com/yezyilomo/django-restql) - Turn your REST API into a GraphQL like API(It allows clients to control which fields will be sent in a response, uses GraphQL like syntax, supports read and write on both flat and nested fields).
- [graphwrap](https://github.com/PaulGilmartin/graph_wrap) - Transform your REST API into a fully compliant GraphQL API with just two lines of code. Leverages [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/) to dynamically build, at runtime, a GraphQL ObjectType for each view in your API.
- [drf-shapeless-serializers](https://github.com/khaledsukkar2/drf-shapeless-serializers) - Dynamically assemble, configure, and shape your Django Rest Framework serializers at runtime, much like connecting Lego bricks.

### Serializer fields

- [drf-compound-fields](https://github.com/estebistec/drf-compound-fields) - Provides "compound" serializer fields, such as lists of simple values.
- [drf-extra-fields](https://github.com/Hipo/drf-extra-fields) - Provides extra serializer fields.
- [django-versatileimagefield](https://github.com/WGBH/django-versatileimagefield) - Provides a drop-in replacement for Django's stock `ImageField` that makes it easy to serve images in multiple sizes/renditions from a single field. For DRF-specific implementation docs, [click here](https://django-versatileimagefield.readthedocs.io/en/latest/drf_integration.html).

### Views

- [django-rest-multiple-models](https://github.com/MattBroach/DjangoRestMultipleModels) - Provides a generic view (and mixin) for sending multiple serialized models and/or querysets via a single API request.
- [drf-typed-views](https://github.com/rsinger86/drf-typed-views) - Use Python type annotations to validate/deserialize request parameters. Inspired by API Star, Hug and FastAPI.
- [rest-framework-actions](https://github.com/AlexisMunera98/rest-framework-actions) - Provides control over each action in ViewSets. Serializers per action, method.

### Routers

- [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - Provides routers and relationship fields for working with nested resources.
- [wq.db.rest](https://wq.io/docs/about-rest) - Provides an admin-style model registration API with reasonable default URLs and viewsets.

### Parsers

- [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack) - Provides MessagePack renderer and parser support.
- [djangorestframework-jsonapi](https://github.com/django-json-api/django-rest-framework-json-api) - Provides a parser, renderer, serializers, and other tools to help build an API that is compliant with the jsonapi.org spec.
- [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case) - Provides camel case JSON renderers and parsers.
- [nested-multipart-parser](https://github.com/remigermain/nested-multipart-parser) - Provides nested parser for http multipart request

### Renderers

- [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv) - Provides CSV renderer support.
- [djangorestframework-jsonapi](https://github.com/django-json-api/django-rest-framework-json-api) - Provides a parser, renderer, serializers, and other tools to help build an API that is compliant with the jsonapi.org spec.
- [drf\_ujson2](https://github.com/Amertz08/drf_ujson2) - Implements JSON rendering using the UJSON package.
- [rest-pandas](https://github.com/wq/django-rest-pandas) - Pandas DataFrame-powered renderers including Excel, CSV, and SVG formats.
- [djangorestframework-rapidjson](https://github.com/allisson/django-rest-framework-rapidjson) - Provides rapidjson support with parser and renderer.

### Filtering

- [djangorestframework-chain](https://github.com/philipn/django-rest-framework-chain) - Allows arbitrary chaining of both relations and lookup filters.
- [django-url-filter](https://github.com/miki725/django-url-filter) - Allows a safe way to filter data via human-friendly URLs. It is a generic library which is not tied to DRF but it provides easy integration with DRF.
- [drf-url-filter](https://github.com/manjitkumar/drf-url-filters) is a simple Django app to apply filters on drf `ModelViewSet`'s `Queryset` in a clean, simple and configurable way. It also supports validations on incoming query params and their values.
- [django-rest-framework-guardian](https://github.com/rpkilby/django-rest-framework-guardian) - Provides integration with django-guardian, including the `DjangoObjectPermissionsFilter` previously found in DRF.

### Misc

- [drf-sendables](https://github.com/amikrop/drf-sendables) - User messages for Django REST Framework
- [cookiecutter-django-rest](https://github.com/agconti/cookiecutter-django-rest) - A cookiecutter template that takes care of the setup and configuration so you can focus on making your REST apis awesome.
- [djangorestrelationalhyperlink](https://github.com/fredkingham/django_rest_model_hyperlink_serializers_project) - A hyperlinked serializer that can can be used to alter relationships via hyperlinks, but otherwise like a hyperlink model serializer.
- [django-rest-framework-proxy](https://github.com/eofs/django-rest-framework-proxy) - Proxy to redirect incoming request to another API server.
- [gaiarestframework](https://github.com/AppsFuel/gaiarestframework) - Utils for django-rest-framework
- [drf-extensions](https://github.com/chibisov/drf-extensions) - A collection of custom extensions
- [ember-django-adapter](https://github.com/dustinfarris/ember-django-adapter) - An adapter for working with Ember.js
- [django-versatileimagefield](https://github.com/WGBH/django-versatileimagefield) - Provides a drop-in replacement for Django's stock `ImageField` that makes it easy to serve images in multiple sizes/renditions from a single field. For DRF-specific implementation docs, [click here](https://django-versatileimagefield.readthedocs.io/en/latest/drf_integration.html).
- [drf-tracking](https://github.com/aschn/drf-tracking) - Utilities to track requests to DRF API views.
- [drf\_tweaks](https://github.com/ArabellaTech/drf_tweaks) - Serializers with one-step validation (and more), pagination without counts and other tweaks.
- [django-rest-framework-braces](https://github.com/dealertrack/django-rest-framework-braces) - Collection of utilities for working with Django Rest Framework. The most notable ones are [FormSerializer](https://django-rest-framework-braces.readthedocs.io/en/latest/overview.html#formserializer) and [SerializerForm](https://django-rest-framework-braces.readthedocs.io/en/latest/overview.html#serializerform), which are adapters between DRF serializers and Django forms.
- [drf-haystack](https://drf-haystack.readthedocs.io/en/latest/) - Haystack search for Django Rest Framework
- [django-rest-framework-version-transforms](https://github.com/mrhwick/django-rest-framework-version-transforms) - Enables the use of delta transformations for versioning of DRF resource representations.
- [django-rest-messaging](https://github.com/raphaelgyory/django-rest-messaging), [django-rest-messaging-centrifugo](https://github.com/raphaelgyory/django-rest-messaging-centrifugo) and [django-rest-messaging-js](https://github.com/raphaelgyory/django-rest-messaging-js) - A real-time pluggable messaging service using DRM.
- [djangorest-alchemy](https://github.com/dealertrack/djangorest-alchemy) - SQLAlchemy support for REST framework.
- [djangorestframework-datatables](https://github.com/izimobil/django-rest-framework-datatables) - Seamless integration between Django REST framework and [Datatables](https://datatables.net).
- [django-rest-framework-condition](https://github.com/jozo/django-rest-framework-condition) - Decorators for managing HTTP cache headers for Django REST framework (ETag and Last-modified).
- [django-rest-witchcraft](https://github.com/shosca/django-rest-witchcraft) - Provides DRF integration with SQLAlchemy with SQLAlchemy model serializers/viewsets and a bunch of other goodies
- [djangorestframework-mvt](https://github.com/corteva/djangorestframework-mvt) - An extension for creating views that serve Postgres data as Map Box Vector Tiles.
- [drf-viewset-profiler](https://github.com/fvlima/drf-viewset-profiler) - Lib to profile all methods from a viewset line by line.
- [djangorestframework-features](https://github.com/cloudcode-hungary/django-rest-framework-features/) - Advanced schema generation and more based on named features.
- [django-elasticsearch-dsl-drf](https://github.com/barseghyanartur/django-elasticsearch-dsl-drf) - Integrate Elasticsearch DSL with Django REST framework. Package provides views, serializers, filter backends, pagination and other handy add-ons.
- [django-lisan](https://github.com/Nabute/django-lisan) - A lightweight translation and localization framework for Django REST Framework APIs.
- [django-api-client](https://github.com/rhenter/django-api-client) - DRF client that groups the Endpoint response, for use in CBVs and FBV as if you were working with Django's Native Models..
- [fast-drf](https://github.com/iashraful/fast-drf) - A model based library for making API development faster and easier.
- [django-requestlogs](https://github.com/Raekkeri/django-requestlogs) - Providing middleware and other helpers for audit logging for REST framework.
- [drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) - DRF exception handler to standardize error responses for all API endpoints.
- [drf-api-action](https://github.com/Ori-Roza/drf-api-action) - uses the power of DRF also as a library functions
- [apitally](https://github.com/apitally/apitally-py) - A simple API monitoring, analytics, and request logging tool using middleware. For DRF-specific setup guide, [click here](https://docs.apitally.io/frameworks/django-rest-framework).
- [wireup](https://github.com/maldoinc/wireup) - Dependency injection container with Django integration support. For integration docs, [click here](https://maldoinc.github.io/wireup/latest/integrations/django/).

### Customization

- [drf-restwind](https://github.com/youzarsiph/drf-restwind) - a modern re-imagining of the Django REST Framework utilizes TailwindCSS and DaisyUI to provide flexible and customizable UI solutions with minimal coding effort.
- [drf-redesign](https://github.com/youzarsiph/drf-redesign) - A project that gives a fresh look to the browse-able API using Bootstrap 5.
- [drf-material](https://github.com/youzarsiph/drf-material) - A project that gives a sleek and elegant look to the browsable API using Material Design.

Back to top