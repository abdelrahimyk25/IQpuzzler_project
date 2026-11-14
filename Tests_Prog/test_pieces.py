import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Game_Element.pieces import PIECES, normaliser, rotation, miroir, generate_catalogue_orient

piece = PIECES["I"]["coords"]

print("Original:", piece)
print("Normalisee:", normaliser(piece))
print("Rotation 90:", rotation(piece))
print("Rotation 180:", rotation(rotation(piece)))
print("Miroir:", miroir(piece))

catalogue = generate_catalogue_orient()

for id_piece, orientations in catalogue.items():
    print(f"Piece {id_piece}: {len(orientations)} orientations")

assert len(PIECES) == 12
assert sum(len(p["coords"]) for p in PIECES.values()) == 55

print("All 12 pieces and 55 balls verified!")