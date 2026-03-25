<!-- Source: https://docs.streamlit.io/develop/concepts/configuration/https-support -->

Many apps need to be accessed with SSL / [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) protocol or `https://`.

We recommend performing SSL termination in a reverse proxy or load balancer for self-hosted and production use cases, not directly in the app. [Streamlit Community Cloud](/deploy/streamlit-community-cloud) uses this approach, and every major cloud and app hosting platform should allow you to configure it and provide extensive documentation. You can find some of these platforms in our [Deployment tutorials](/deploy/tutorials).

To terminate SSL in your Streamlit app, you must configure `server.sslCertFile` and `server.sslKeyFile`. Learn how to set config options in [Configuration](/develop/concepts/configuration).

- The configuration value should be a local file path to a cert file and key file. These must be available at the time the app starts.
- Both `server.sslCertFile` and `server.sslKeyFile` must be specified. If only one is specified, your app will exit with an error.
- This feature will not work in Community Cloud. Community Cloud already serves your app with TLS.

In a production environment, we recommend performing SSL termination by the load balancer or the reverse proxy, not using this option. The use of this option in Streamlit has not gone through extensive security audits or performance tests.

```
# .streamlit/config.toml

[server]
sslCertFile = '/path/to/certchain.pem'
sslKeyFile = '/path/to/private.key'
```

[*arrow\_back*Previous: Configuration options](/develop/concepts/configuration/options)[*arrow\_forward*Next: Serving static files](/develop/concepts/configuration/serving-static-files)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI