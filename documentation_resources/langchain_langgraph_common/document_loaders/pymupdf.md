<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/pymupdf -->

This notebook provides a quick overview for getting started with `PyMuPDF` [document loader](https://python.langchain.com/docs/concepts/document_loaders). For detailed documentation of all \_\_ModuleName\_\_Loader features and configurations head to the [API reference](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyMuPDFLoader.html).

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| [PyMuPDFLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyMuPDFLoader.html) | [langchain-community](https://python.langchain.com/api_reference/community/index.html) | ✅ | ❌ | ❌ |

---

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support | Extract Images | Extract Tables |
| --- | --- | --- | --- | --- |
| PyMuPDFLoader | ✅ | ❌ | ✅ | ✅ |

## [​](#setup) Setup

### [​](#credentials) Credentials

No credentials are required to use PyMuPDFLoader
If you want to get automated best in-class tracing of your model calls you can also set your [LangSmith](https://docs.smith.langchain.com/) API key by uncommenting below:

Copy

```
# os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
# os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

Install **langchain-community** and **pymupdf**.

Copy

```
%pip install -qU langchain-community pymupdf
```

Copy

```
Note: you may need to restart the kernel to use updated packages.
```

## [​](#initialization) Initialization

Now we can instantiate our model object and load documents:

Copy

```
from langchain_community.document_loaders import PyMuPDFLoader

file_path = "./example_data/layout-parser-paper.pdf"
loader = PyMuPDFLoader(file_path)
```

## [​](#load) Load

Copy

```
docs = loader.load()
docs[0]
```

Copy

```
Document(metadata={'producer': 'pdfTeX-1.40.21', 'creator': 'LaTeX with hyperref', 'creationdate': '2021-06-22T01:27:10+00:00', 'source': './example_data/layout-parser-paper.pdf', 'file_path': './example_data/layout-parser-paper.pdf', 'total_pages': 16, 'format': 'PDF 1.5', 'title': '', 'author': '', 'subject': '', 'keywords': '', 'moddate': '2021-06-22T01:27:10+00:00', 'trapped': '', 'page': 0}, page_content='LayoutParser: A Uniﬁed Toolkit for Deep\nLearning Based Document Image Analysis\nZejiang Shen1 (\x00), Ruochen Zhang2, Melissa Dell3, Benjamin Charles Germain\nLee4, Jacob Carlson3, and Weining Li5\n1 Allen Institute for AI\nshannons@allenai.org\n2 Brown University\nruochen zhang@brown.edu\n3 Harvard University\n{melissadell,jacob carlson}@fas.harvard.edu\n4 University of Washington\nbcgl@cs.washington.edu\n5 University of Waterloo\nw422li@uwaterloo.ca\nAbstract. Recent advances in document image analysis (DIA) have been\nprimarily driven by the application of neural networks. Ideally, research\noutcomes could be easily deployed in production and extended for further\ninvestigation. However, various factors like loosely organized codebases\nand sophisticated model conﬁgurations complicate the easy reuse of im-\nportant innovations by a wide audience. Though there have been on-going\neﬀorts to improve reusability and simplify deep learning (DL) model\ndevelopment in disciplines like natural language processing and computer\nvision, none of them are optimized for challenges in the domain of DIA.\nThis represents a major gap in the existing toolkit, as DIA is central to\nacademic research across a wide range of disciplines in the social sciences\nand humanities. This paper introduces LayoutParser, an open-source\nlibrary for streamlining the usage of DL in DIA research and applica-\ntions. The core LayoutParser library comes with a set of simple and\nintuitive interfaces for applying and customizing DL models for layout de-\ntection, character recognition, and many other document processing tasks.\nTo promote extensibility, LayoutParser also incorporates a community\nplatform for sharing both pre-trained models and full document digiti-\nzation pipelines. We demonstrate that LayoutParser is helpful for both\nlightweight and large-scale digitization pipelines in real-word use cases.\nThe library is publicly available at https://layout-parser.github.io.\nKeywords: Document Image Analysis · Deep Learning · Layout Analysis\n· Character Recognition · Open Source library · Toolkit.\n1\nIntroduction\nDeep Learning(DL)-based approaches are the state-of-the-art for a wide range of\ndocument image analysis (DIA) tasks including document image classiﬁcation [11,\narXiv:2103.15348v2  [cs.CV]  21 Jun 2021')
```

Copy

```
import pprint

pprint.pp(docs[0].metadata)
```

Copy

```
{'producer': 'pdfTeX-1.40.21',
 'creator': 'LaTeX with hyperref',
 'creationdate': '2021-06-22T01:27:10+00:00',
 'source': './example_data/layout-parser-paper.pdf',
 'file_path': './example_data/layout-parser-paper.pdf',
 'total_pages': 16,
 'format': 'PDF 1.5',
 'title': '',
 'author': '',
 'subject': '',
 'keywords': '',
 'moddate': '2021-06-22T01:27:10+00:00',
 'trapped': '',
 'page': 0}
```

## [​](#lazy-load) Lazy load

Copy

```
pages = []
for doc in loader.lazy_load():
    pages.append(doc)
    if len(pages) >= 10:
        # do some paged operation, e.g.
        # index.upsert(page)

        pages = []
len(pages)
```

Copy

```
6
```

Copy

```
print(pages[0].page_content[:100])
pprint.pp(pages[0].metadata)
```

Copy

```
LayoutParser: A Uniﬁed Toolkit for DL-Based DIA
11
focuses on precision, eﬃciency, and robustness. T
{'producer': 'pdfTeX-1.40.21',
 'creator': 'LaTeX with hyperref',
 'creationdate': '2021-06-22T01:27:10+00:00',
 'source': './example_data/layout-parser-paper.pdf',
 'file_path': './example_data/layout-parser-paper.pdf',
 'total_pages': 16,
 'format': 'PDF 1.5',
 'title': '',
 'author': '',
 'subject': '',
 'keywords': '',
 'moddate': '2021-06-22T01:27:10+00:00',
 'trapped': '',
 'page': 10}
```

The metadata attribute contains at least the following keys:

- source
- page (if in mode *page*)
- total\_page
- creationdate
- creator
- producer

Additional metadata are specific to each parser.
These pieces of information can be helpful (to categorize your PDFs for example).

## [​](#splitting-mode-&-custom-pages-delimiter) Splitting mode & custom pages delimiter

When loading the PDF file you can split it in two different ways:

- By page
- As a single text flow

By default PyMuPDFLoader will split the PDF by page.

### [​](#extract-the-pdf-by-page-each-page-is-extracted-as-a-langchain-document-object) Extract the PDF by page. each page is extracted as a langchain document object

Copy

```
loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="page",
)
docs = loader.load()
print(len(docs))
pprint.pp(docs[0].metadata)
```

Copy

```
16
{'producer': 'pdfTeX-1.40.21',
 'creator': 'LaTeX with hyperref',
 'creationdate': '2021-06-22T01:27:10+00:00',
 'source': './example_data/layout-parser-paper.pdf',
 'file_path': './example_data/layout-parser-paper.pdf',
 'total_pages': 16,
 'format': 'PDF 1.5',
 'title': '',
 'author': '',
 'subject': '',
 'keywords': '',
 'moddate': '2021-06-22T01:27:10+00:00',
 'trapped': '',
 'page': 0}
```

In this mode the pdf is split by pages and the resulting Documents metadata contains the page number. But in some cases we could want to process the pdf as a single text flow (so we don’t cut some paragraphs in half). In this case you can use the *single* mode :

### [​](#extract-the-whole-pdf-as-a-single-langchain-document-object) Extract the whole PDF as a single langchain document object

Copy

```
loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="single",
)
docs = loader.load()
print(len(docs))
pprint.pp(docs[0].metadata)
```

Copy

```
1
{'producer': 'pdfTeX-1.40.21',
 'creator': 'LaTeX with hyperref',
 'creationdate': '2021-06-22T01:27:10+00:00',
 'source': './example_data/layout-parser-paper.pdf',
 'file_path': './example_data/layout-parser-paper.pdf',
 'total_pages': 16,
 'format': 'PDF 1.5',
 'title': '',
 'author': '',
 'subject': '',
 'keywords': '',
 'moddate': '2021-06-22T01:27:10+00:00',
 'trapped': ''}
```

Logically, in this mode, the ‘page\_number’ metadata disappears. Here’s how to clearly identify where pages end in the text flow :

### [​](#add-a-custom-pages_delimiter-to-identify-where-are-ends-of-pages-in-single-mode) Add a custom *pages\_delimiter* to identify where are ends of pages in *single* mode

Copy

```
loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="single",
    pages_delimiter="\n-------THIS IS A CUSTOM END OF PAGE-------\n",
)
docs = loader.load()
print(docs[0].page_content[:5780])
```

This could simply be \n, or \f to clearly indicate a page change, or <!— PAGE BREAK —> for seamless injection in a Markdown viewer without a visual effect.

# [​](#extract-images-from-the-pdf) Extract images from the PDF

You can extract images from your PDFs with a choice of three different solutions:

- rapidOCR (lightweight Optical Character Recognition tool)
- Tesseract (OCR tool with high precision)
- Multimodal language model

You can tune these functions to choose the output format of the extracted images among *html*, *markdown* or *text*
The result is inserted between the last and the second-to-last paragraphs of text of the page.

### [​](#extract-images-from-the-pdf-with-rapidocr) Extract images from the PDF with rapidOCR

Copy

```
%pip install -qU rapidocr-onnxruntime
```

Copy

```
Note: you may need to restart the kernel to use updated packages.
```

Copy

```
from langchain_community.document_loaders.parsers import RapidOCRBlobParser

loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="page",
    images_inner_format="markdown-img",
    images_parser=RapidOCRBlobParser(),
)
docs = loader.load()

print(docs[5].page_content)
```

Be careful, RapidOCR is designed to work with Chinese and English, not other languages.

### [​](#extract-images-from-the-pdf-with-tesseract) Extract images from the PDF with tesseract

Copy

```
%pip install -qU pytesseract
```

Copy

```
Note: you may need to restart the kernel to use updated packages.
```

Copy

```
from langchain_community.document_loaders.parsers import TesseractBlobParser

loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="page",
    images_inner_format="html-img",
    images_parser=TesseractBlobParser(),
)
docs = loader.load()
print(docs[5].page_content)
```

### [​](#extract-images-from-the-pdf-with-multimodal-model) Extract images from the PDF with multimodal model

Copy

```
%pip install -qU langchain-openai
```

Copy

```
Note: you may need to restart the kernel to use updated packages.
```

Copy

```
import os

from dotenv import load_dotenv

load_dotenv()
```

Copy

```
True
```

Copy

```
from getpass import getpass

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass("OpenAI API key =")
```

Copy

```
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_openai import ChatOpenAI

loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="page",
    images_inner_format="markdown-img",
    images_parser=LLMImageBlobParser(model=ChatOpenAI(model="gpt-4o", max_tokens=1024)),
)
docs = loader.load()
print(docs[5].page_content)
```

# [​](#extract-tables-from-the-pdf) Extract tables from the PDF

With PyMUPDF you can extract tables from your PDFs in *html*, *markdown* or *csv* format :

Copy

```
loader = PyMuPDFLoader(
    "./example_data/layout-parser-paper.pdf",
    mode="page",
    extract_tables="markdown",
)
docs = loader.load()
print(docs[4].page_content)
```

Copy

```
LayoutParser: A Uniﬁed Toolkit for DL-Based DIA
5
Table 1: Current layout detection models in the LayoutParser model zoo
Dataset
Base Model1 Large Model
Notes
PubLayNet [38]
F / M
M
Layouts of modern scientiﬁc documents
PRImA [3]
M
-
Layouts of scanned modern magazines and scientiﬁc reports
Newspaper [17]
F
-
Layouts of scanned US newspapers from the 20th century
TableBank [18]
F
F
Table region on modern scientiﬁc and business document
HJDataset [31]
F / M
-
Layouts of history Japanese documents
1 For each dataset, we train several models of diﬀerent sizes for diﬀerent needs (the trade-oﬀbetween accuracy
vs. computational cost). For “base model” and “large model”, we refer to using the ResNet 50 or ResNet 101
backbones [13], respectively. One can train models of diﬀerent architectures, like Faster R-CNN [28] (F) and Mask
R-CNN [12] (M). For example, an F in the Large Model column indicates it has a Faster R-CNN model trained
using the ResNet 101 backbone. The platform is maintained and a number of additions will be made to the model
zoo in coming months.
layout data structures, which are optimized for eﬃciency and versatility. 3) When
necessary, users can employ existing or customized OCR models via the uniﬁed
API provided in the OCR module. 4) LayoutParser comes with a set of utility
functions for the visualization and storage of the layout data. 5) LayoutParser
is also highly customizable, via its integration with functions for layout data
annotation and model training. We now provide detailed descriptions for each
component.
3.1
Layout Detection Models
In LayoutParser, a layout model takes a document image as an input and
generates a list of rectangular boxes for the target content regions. Diﬀerent
from traditional methods, it relies on deep convolutional neural networks rather
than manually curated rules to identify content regions. It is formulated as an
object detection problem and state-of-the-art models like Faster R-CNN [28] and
Mask R-CNN [12] are used. This yields prediction results of high accuracy and
makes it possible to build a concise, generalized interface for layout detection.
LayoutParser, built upon Detectron2 [35], provides a minimal API that can
perform layout detection with only four lines of code in Python:
1 import
layoutparser as lp
2 image = cv2.imread("image_file") # load
images
3 model = lp. Detectron2LayoutModel (
4
"lp:// PubLayNet/ faster_rcnn_R_50_FPN_3x /config")
5 layout = model.detect(image)
LayoutParser provides a wealth of pre-trained model weights using various
datasets covering diﬀerent languages, time periods, and document types. Due to
domain shift [7], the prediction performance can notably drop when models are ap-
plied to target samples that are signiﬁcantly diﬀerent from the training dataset. As
document structures and layouts vary greatly in diﬀerent domains, it is important
to select models trained on a dataset similar to the test samples. A semantic syntax
is used for initializing the model weights in LayoutParser, using both the dataset
name and model name lp://<dataset-name>/<model-architecture-name>.

|Dataset|Base Model1|Large Model|Notes|
|---|---|---|---|
|PubLayNet [38] PRImA [3] Newspaper [17] TableBank [18] HJDataset [31]|F / M M F F F / M|M &amp;#45; &amp;#45; F &amp;#45;|Layouts of modern scientific documents Layouts of scanned modern magazines and scientific reports Layouts of scanned US newspapers from the 20th century Table region on modern scientific and business document Layouts of history Japanese documents|
```

## [​](#working-with-files) Working with files

Many document loaders involve parsing files. The difference between such loaders usually stems from how the file is parsed, rather than how the file is loaded. For example, you can use `open` to read the binary content of either a PDF or a markdown file, but you need different parsing logic to convert that binary data into text.
As a result, it can be helpful to decouple the parsing logic from the loading logic, which makes it easier to reuse a given parser regardless of how the data was loaded.
You can use this strategy to analyze different files, with the same parsing parameters.

Copy

```
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyMuPDFParser

loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path="./example_data/",
        glob="*.pdf",
    ),
    blob_parser=PyMuPDFParser(),
)
docs = loader.load()
print(docs[0].page_content)
pprint.pp(docs[0].metadata)
```

Copy

```
LayoutParser: A Uniﬁed Toolkit for Deep
Learning Based Document Image Analysis
Zejiang Shen1 (�), Ruochen Zhang2, Melissa Dell3, Benjamin Charles Germain
Lee4, Jacob Carlson3, and Weining Li5
1 Allen Institute for AI
shannons@allenai.org
2 Brown University
ruochen zhang@brown.edu
3 Harvard University
{melissadell,jacob carlson}@fas.harvard.edu
4 University of Washington
bcgl@cs.washington.edu
5 University of Waterloo
w422li@uwaterloo.ca
Abstract. Recent advances in document image analysis (DIA) have been
primarily driven by the application of neural networks. Ideally, research
outcomes could be easily deployed in production and extended for further
investigation. However, various factors like loosely organized codebases
and sophisticated model conﬁgurations complicate the easy reuse of im-
portant innovations by a wide audience. Though there have been on-going
eﬀorts to improve reusability and simplify deep learning (DL) model
development in disciplines like natural language processing and computer
vision, none of them are optimized for challenges in the domain of DIA.
This represents a major gap in the existing toolkit, as DIA is central to
academic research across a wide range of disciplines in the social sciences
and humanities. This paper introduces LayoutParser, an open-source
library for streamlining the usage of DL in DIA research and applica-
tions. The core LayoutParser library comes with a set of simple and
intuitive interfaces for applying and customizing DL models for layout de-
tection, character recognition, and many other document processing tasks.
To promote extensibility, LayoutParser also incorporates a community
platform for sharing both pre-trained models and full document digiti-
zation pipelines. We demonstrate that LayoutParser is helpful for both
lightweight and large-scale digitization pipelines in real-word use cases.
The library is publicly available at https://layout-parser.github.io.
Keywords: Document Image Analysis · Deep Learning · Layout Analysis
· Character Recognition · Open Source library · Toolkit.
1
Introduction
Deep Learning(DL)-based approaches are the state-of-the-art for a wide range of
document image analysis (DIA) tasks including document image classiﬁcation [11,
arXiv:2103.15348v2  [cs.CV]  21 Jun 2021
{'source': 'example_data/layout-parser-paper.pdf',
 'file_path': 'example_data/layout-parser-paper.pdf',
 'total_pages': 16,
 'format': 'PDF 1.5',
 'title': '',
 'author': '',
 'subject': '',
 'keywords': '',
 'creator': 'LaTeX with hyperref',
 'producer': 'pdfTeX-1.40.21',
 'creationdate': '2021-06-22T01:27:10+00:00',
 'moddate': '2021-06-22T01:27:10+00:00',
 'trapped': '',
 'page': 0}
```

It is possible to work with files from cloud storage.

Copy

```
from langchain_community.document_loaders import CloudBlobLoader
from langchain_community.document_loaders.generic import GenericLoader

loader = GenericLoader(
    blob_loader=CloudBlobLoader(
        url="s3:/mybucket",  # Supports s3://, az://, gs://, file:// schemes.
        glob="*.pdf",
    ),
    blob_parser=PyMuPDFParser(),
)
docs = loader.load()
print(docs[0].page_content)
pprint.pp(docs[0].metadata)
```

## [​](#api-reference) API reference

For detailed documentation of all `PyMuPDFLoader` features and configurations head to the API reference: [python.langchain.com/api\_reference/community/document\_loaders/langchain\_community.document\_loaders.pdf.PyMuPDFLoader.html](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyMuPDFLoader.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/pymupdf.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.