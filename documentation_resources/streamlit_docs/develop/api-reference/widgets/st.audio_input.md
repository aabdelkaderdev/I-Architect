<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.audio_input -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/audio_input.py#L90 "View st.audio_input source code on GitHub") | |
| --- | --- |
| st.audio\_input(label, \*, sample\_rate=16000, key=None, help=None, on\_change=None, args=None, kwargs=None, disabled=False, label\_visibility="visible", width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this widget is used for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| sample\_rate (int or None) | The target sample rate for the audio recording in Hz. This defaults to 16000, which is optimal for speech recognition.  The following values are supported: 8000 (telephone quality), 11025, 16000 (speech-recognition quality), 22050, 24000, 32000, 44100, 48000 (high-quality), or None. If this is None, the widget uses the browser's default sample rate (typically 44100 or 48000 Hz). |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  A key lets you access the widget's value via st.session\_state[key] (read-only). For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this audio input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the audio input if set to True. Default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the audio input widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the   width of the parent container. - An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (None or UploadedFile) | The UploadedFile class is a subclass of BytesIO, and therefore is "file-like". This means you can pass an instance of it anywhere a file is expected. The MIME type for the audio data is audio/wav.  Note  The resulting UploadedFile is subject to the size limitation configured in server.maxUploadSize. If you expect large sound files, update the configuration option appropriately. |

#### Examples

*Example 1:* Record a voice message and play it back.\*

The default sample rate of 16000 Hz is optimal for speech recognition.

```
import streamlit as st

audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-audio-input.streamlit.app//?utm_medium=oembed&)

*Example 2:* Record high-fidelity audio and play it back.\*

Higher sample rates can create higher-quality, larger audio files. This
might require a nicer microphone to fully appreciate the difference.

```
import streamlit as st

audio_value = st.audio_input("Record high quality audio", sample_rate=48000)

if audio_value:
    st.audio(audio_value)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-audio-input-high-rate.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.text\_input](/develop/api-reference/widgets/st.text_input)[*arrow\_forward*Next: st.camera\_input](/develop/api-reference/widgets/st.camera_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI