# Bangladesh Railway Information Dataset

## Overview

This repository contains data related to trains, coaches, and railway stations in Bangladesh. The information is provided in both English and Bengali, formatted as JSON files.

## Files

- **`trains_en.json`**: Train names and numbers in English.
- **`trains_bn.json`**: Train names and numbers in Bengali.
- **`coaches_en.json`**: Coach names in English.
- **`coaches_bn.json`**: Coach names in Bengali.
- **`stations_en.json`**: Station names in English.
- **`stations_bn.json`**: Station names in Bengali.

## Example Data

### Train Data
- English: "AGHNIBINA EXPRESS (735)"
- Bengali: "অগ্নিবীণা এক্সপ্রেস (৭৩৫)"

### Coach Codes
- English: "KA", "XTR1"
- Bengali: "ক", "এক্সট্রা-১"

### Station Names
- English: "Dhaka", "Chattogram"
- Bengali: "ঢাকা", "চট্টগ্রাম"

## How to Use

1. Load the data in your project using JSON libraries in any programming language.
2. Utilize the data for applications like train schedules, ticket booking systems, or railway analysis.

### Python Example
```python
import json

# Load train data in English
with open('trains_en.json') as file:
    trains = json.load(file)
    print(trains["trains"])

# Load station data in Bengali
with open('stations_bn.json') as file:
    stations = json.load(file)
    print(stations["stations"])
```

## Contribution

Contributions are welcome! Fork the repo, make your changes, and create a pull request.