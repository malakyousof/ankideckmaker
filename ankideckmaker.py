import pdfplumber
import pandas as pd
import os
import genanki

# Path to the PDF file
pdf_path = "D:\\nnlt\\backendlearning\\pythonProject\\Vocabulary_of_JLPT_N5.pdf"  # replace this with you pdf file

data = []


with pdfplumber.open(pdf_path) as pdf:
    row_count = 0  #starting index is 0
    for page in pdf.pages:
        table = page.extract_table() #extract the pages (my pdf is structred)
        if table:
            for row in table:
                if len(row) >= 4:  # Ensure there are at least 3 columns
                    #columns 1 (hiragana) and 2 (meaning) (i skipped kanji it errored from alll null)
                    data.append([row[1], row[3]]) #this is the 2 rows i wanted , again chnage this according to you
                    row_count += 1

                    if row_count >= 300: #for my own learning purposes i only needed the fist 300  "rows" aka words
                        break
        if row_count >= 300: #you can adjust or remove it completely
            break
#######################################################################
#making it csv formate (so its compatible with anki )
df = pd.DataFrame(data, columns=["hiragana", "meaning"])

#from csv to deck

# model for the deck
my_model = genanki.Model(
    1607392319,  #unique id
    'Basic Model', #type of model
    fields=[{'name': 'Front'}, {'name': 'Back'}],
    templates=[ #making the cards here, you tweak as much you want here)
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',  # Question (Hiragana)
            'afmt': '{{Back}}',   # Answer (Meaning)
        },
    ])


my_deck = genanki.Deck(
    2059400110,  #unique id
    'JLPT N5 Vocabulary Deck' #name it
)

#actually adding the cards
for _, row in df.iterrows():
    #so it wont error out (genkai like panda cant handle empty/messing data. you replace with none or no data etc
    hiragana = row['hiragana'] if row['hiragana'] is not None else ""
    meaning = row['meaning'] if row['meaning'] is not None else ""


    my_deck.add_note(genanki.Note(
        model=my_model,
        fields=[hiragana, meaning]  # Hiragana -> Front, Meaning -> Back
    ))

# Save the deck as an .apkg file
output_deck_file = "n5deck_anki2.apkg"
my_deck.write_to_file(output_deck_file)

print(f"Anki deck saved to {output_deck_file}")

full_path = os.path.abspath(output_deck_file)

# Print the path (notes: do it i couldnt find the file lol)
print(f"Anki deck saved to {full_path}")
