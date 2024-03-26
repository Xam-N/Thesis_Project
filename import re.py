import re

custom_tags = {
  "unitCode": r"\b[A-Z]{4}[0-9]{4}\b",
  "dash": r"-",
  "unitYear": r"\b[0-9]{4}\b",  # Changed the pattern to match any 4-digit number
  "level": r"\b[0-9]{4}\b",      # Changed the pattern to match any 4-digit number
  "bool": r"\bor\b|\band\b|\binclude\b|\b,\b",
  "inequal": r"\babove\b",
}

def tagDescription(data):
    words = data.split()
    labels = set()  # Use a set to ensure unique labels for each string
    for word in words:
        for type_label, pattern in custom_tags.items():
            if re.match(pattern, word):
                labels.add(type_label)

    return list(labels)

# Define sample strings
samples = [
    "COMP3100 - something else",
    "COMP1000 - ENGG1000",
    "3000 level and above",
    "COMP3100 or COMP1000"
]

# Label each sample string
for i, sample in enumerate(samples):
    labels = tagDescription(sample)
    print(f"Sample {i+1}: {sample} - Labels: {labels}")