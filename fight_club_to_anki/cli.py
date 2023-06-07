import xml.etree.ElementTree as ET
from pathlib import Path

import genanki


def load(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return root


def dump(filepath, content):
    deck = genanki.Deck(
        deck_id=1234,
        name=Path(filepath).stem,
    )

    model = genanki.Model(
        model_id=123,
        name="thing",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[
            {
                "name": "Card One",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            }
        ],
    )

    for field in ["note", "item", "feat"]:
        for i in content.iter(field):
            name = i.find("name").text
            attr = next(
                (n for n in ["text", "quantity"] if i.find(n) is not None), None
            )
            print(name, attr)
            deck.add_note(genanki.Note(model=model, fields=[name, i.find(attr).text]))

    genanki.Package(deck).write_to_file(filepath)


if __name__ == "__main__":
    import sys

    source_file, destination_file = sys.argv[-2:]

    dump(destination_file, load(source_file))
