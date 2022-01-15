## JSON Data

### Wikipedia Definition

`Json` (JavaScript Object Notation, pronounced `/jaysawn/;`) is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values). It is a common data format with diverse uses in electronic data interchange, including that of web applications with servers.

`Json` is a language-independent data format. It was derived from JavaScript, but many modern programming languages include code to generate and parse Json-format data. `json` filenames use the extension `.json` .<sup>[1]</sup>

### Motivation

Being `language-independant` is very important. Language-independance means that some or all programming languages can interact with (in this case) `json`. The reason this is possible is that `json` follows a set of predefined rules for storage, otherwise known as a `standard`. 

Most contemporary programming languages have a `json` library. This allows you to write out a `json` file in one language, and read it in using another. This is not groundbreaking since there does exist other file formats that allow similar behavior: `csv` and `xml` come to mind. Without getting into a head to head comparison, each have their own upsides and downsides. 

### Json Overview

Let me cover json using examples. Json really breaks down to `key`:`value` pairs. Where a `key` is a string identifier (like a variable name) that is associated with a value. The value can be:
- integer
- float
- string
- array
- onother json object

```json
key:value
\\ or
"apples":204
```

#### Examples

I will use Python to help explain Json. It's lists and dictionaries line up well with Json syntax.

Simple **key:value** pair

```python
ex1 = {
    "itemCount":100
}


```

The curly braces are what define the object. 



[1] https://en.wikipedia.org/wiki/JSON