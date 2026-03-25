<!-- Source: https://docs.streamlit.io/develop/api-reference/media/st.video -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/media.py#L224 "View st.video source code on GitHub") | |
| --- | --- |
| st.video(data, format="video/mp4", start\_time=0, \*, subtitles=None, end\_time=None, loop=False, autoplay=False, muted=False, width="stretch") | |
| Parameters | |
| data (str, Path, bytes, io.BytesIO, numpy.ndarray, or file) | The video to play. This can be one of the following:   - A URL (string) for a hosted video file, including YouTube URLs. - A path to a local video file. The path can be a str   or Path object. Paths can be absolute or relative to the   working directory (where you execute streamlit run). - Raw video data. Raw data formats must include all necessary file   headers to match the file format specified via format. |
| format (str) | The MIME type for the video file. This defaults to "video/mp4". For more information about MIME types, see <https://www.iana.org/assignments/media-types/media-types.xhtml>. |
| start\_time (int, float, timedelta, str, or None) | The time from which the element should start playing. This can be one of the following:   - None (default): The element plays from the beginning. - An int or float specifying the time in seconds. float   values are rounded down to whole seconds. - A string specifying the time in a format supported by [Pandas'   Timedelta constructor](https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html),   e.g. "2 minute", "20s", or "1m14s". - A timedelta object from [Python's built-in datetime library](https://docs.python.org/3/library/datetime.html#timedelta-objects),   e.g. timedelta(seconds=70). |
| subtitles (str, bytes, Path, io.BytesIO, or dict) | Optional subtitle data for the video, supporting several input types:   - None (default): No subtitles. - A string, bytes, or Path: File path to a subtitle file in   .vtt or .srt formats, or the raw content of subtitles   conforming to these formats. Paths can be absolute or relative to   the working directory (where you execute streamlit run).   If providing raw content, the string must adhere to the WebVTT or   SRT format specifications. - io.BytesIO: A BytesIO stream that contains valid .vtt or .srt   formatted subtitle data. - A dictionary: Pairs of labels and file paths or raw subtitle content in   .vtt or .srt formats to enable multiple subtitle tracks.   The label will be shown in the video player. Example:   {"English": "path/to/english.vtt", "French": "path/to/french.srt"}   When provided, subtitles are displayed by default. For multiple tracks, the first one is displayed by default. If you don't want any subtitles displayed by default, use an empty string for the value in a dictrionary's first pair: {"None": "", "English": "path/to/english.vtt"}  Not supported for YouTube videos. |
| end\_time (int, float, timedelta, str, or None) | The time at which the element should stop playing. This can be one of the following:   - None (default): The element plays through to the end. - An int or float specifying the time in seconds. float   values are rounded down to whole seconds. - A string specifying the time in a format supported by [Pandas'   Timedelta constructor](https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html),   e.g. "2 minute", "20s", or "1m14s". - A timedelta object from [Python's built-in datetime library](https://docs.python.org/3/library/datetime.html#timedelta-objects),   e.g. timedelta(seconds=70). |
| loop (bool) | Whether the video should loop playback. |
| autoplay (bool) | Whether the video should start playing automatically. This is False by default. Browsers will not autoplay unmuted videos if the user has not interacted with the page by clicking somewhere. To enable autoplay without user interaction, you must also set muted=True. |
| muted (bool) | Whether the video should play with the audio silenced. This is False by default. Use this in conjunction with autoplay=True to enable autoplay without user interaction. |
| width ("stretch" or int) | The width of the video player element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

video_file = open("myvideo.mp4", "rb")
video_bytes = video_file.read()

st.video(video_bytes)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-video.streamlit.app//?utm_medium=oembed&)

When you include subtitles, they will be turned on by default. A viewer
can turn off the subtitles (or captions) from the browser's default video
control menu, usually located in the lower-right corner of the video.

Here is a simple VTT file (subtitles.vtt):

```
WEBVTT

0:00:01.000 --> 0:00:02.000
Look!

0:00:03.000 --> 0:00:05.000
Look at the pretty stars!
```

If the above VTT file lives in the same directory as your app, you can
add subtitles like so:

```
import streamlit as st

VIDEO_URL = "https://example.com/not-youtube.mp4"
st.video(VIDEO_URL, subtitles="subtitles.vtt")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-video-subtitles.streamlit.app//?utm_medium=oembed&)

See additional examples of supported subtitle input types in our
[video subtitles feature demo](https://doc-video-subtitle-inputs.streamlit.app/).

Note

Some videos may not display if they are encoded using MP4V (which is an export option in OpenCV),
as this codec is not widely supported by browsers. Converting your video to H.264 will allow
the video to be displayed in Streamlit.
See this [StackOverflow post](https://stackoverflow.com/a/49535220/2394542) or this
[Streamlit forum post](https://discuss.streamlit.io/t/st-video-doesnt-show-opencv-generated-mp4/3193/2)
for more information.

[*arrow\_back*Previous: st.pdf](/develop/api-reference/media/st.pdf)[*arrow\_forward*Next: Layouts and containers](/develop/api-reference/layout)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI