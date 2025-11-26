# json-to-flashcards

A quick little script to take a json file with catergories of questions and answers 

## Dependencies

`python 3.10`

```bash
pip install reportlab
```

## JSON Format

```json
{
    "flashcards": {
      "Section 1": [
        {
          "question": "Enter your first question here",
          "answer": "Enter the corresponding answer here"
        },
        {
          "question": "Enter your second question here",
          "answer": "Enter its answer here"
        }
      ],
      "Section 2": [
        {
          "question": "Another section’s question",
          "answer": "And its answer"
        }
      ]
    }
} 
```

## Run it

```bash
py flashcards_to_pdf.py your_flashcards.json
```

The pdf will be saved with the same name as the provided json