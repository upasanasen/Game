"""Merge data/regions/*.json into index.html.

Run from anywhere after editing a country file:  python3 tools/build_regions.py
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "regions")
PAGE = os.path.join(ROOT, "index.html")
ITEM_IDS = ["banana", "eggshell", "coffee", "bones", "shampoo", "polybag", "chips", "tube", "carton",
            "eggtray", "box", "pizza", "newspaper", "jar", "wine", "perfume", "tin", "window", "drinkglass",
            "mirror", "tissue", "diaper", "pad", "battery", "bulb", "meds", "paint", "toy"]
PATS = ["stripes", "dots", "grid", "zigzag", "checks", "waves", "cross", "hbars", "rings"]

# first keyword match wins; checked against "id label sub"
GLYPHS = [
    ("sanitary", "drop"), ("pharmac", "cross"), ("medic", "cross"), ("sigre", "cross"),
    ("batter", "battery"), ("textile", "shirt"), ("cloth", "shirt"), ("store", "bag"), ("bag drop", "bag"),
    ("hazard", "warn"), ("special", "warn"), ("depot", "truck"), ("centre", "truck"), ("center", "truck"),
    ("station", "truck"), ("punto", "truck"), ("déchetterie", "truck"), ("isola", "truck"), ("drop-off", "truck"),
    ("carton", "carton"), ("glass", "jar"), ("vetro", "jar"), ("metal", "can"),
    ("cardboard", "box"), ("paper", "paper"), ("carta", "paper"), ("plastic", "bottle"),
    ("food", "apple"), ("bio", "leaf"), ("organic", "leaf"), ("wet", "leaf"), ("compost", "leaf"), ("green", "leaf"),
    ("residual", "flame"), ("general", "flame"), ("mixed", "flame"), ("rest", "trash"), ("trash", "trash"),
    ("garbage", "trash"), ("landfill", "trash"), ("recycl", "recycle"), ("dry", "recycle"), ("packag", "recycle"),
]


# Short on-bin labels and icons, set by hand. Local names move into the description line.
OVERRIDES = {
    "canada": {"blue": ("Blue bin", "recycle"), "green": ("Green bin", "leaf"), "garbage": ("Garbage", "trash"),
               "depot": ("Hazardous depot", "warn"), "pharmacy": ("Pharmacy", "cross")},
    "denmark": {"food": ("Food waste", "apple"), "paper": ("Paper", "paper"), "cardboard": ("Cardboard", "box", "Boxes and egg trays"),
                "cartons": ("Cartons", "carton"), "glass": ("Glass", "jar"), "metal": ("Metal", "can"),
                "plastic": ("Plastic", "bottle"), "hazardous": ("Hazardous", "warn"), "general": ("Residual", "flame")},
    "finland": {"bio": ("Biowaste", "leaf"), "cardboard": ("Cardboard", "box", "Kartonki: cartons, boxes, trays"),
                "paper": ("Paper", "paper"), "glass": ("Glass", "jar"), "metal": ("Metal", "can"),
                "plastic": ("Plastic", "bottle"), "general": ("Mixed waste", "flame"), "hazardous": ("Hazardous", "warn"),
                "pharmacy": ("Pharmacy", "cross")},
    "france": {"yellow": ("Yellow bin", "recycle", "Emballages: all packaging, paper"), "glass": ("Glass bank", "jar", "Verre: bottles, jars, pots"),
               "bio": ("Brown bin", "leaf", "Biodéchets: food scraps, grounds"), "residual": ("Grey bin", "trash", "Ordures ménagères: the rest"),
               "store": ("Shop drop-off", "battery", "Piles & ampoules: batteries, bulbs"), "pharmacy": ("Pharmacy", "cross", "Cyclamed: unused medicines"),
               "dechetterie": ("Déchèterie", "truck", "Paint, flat glass, bulky items")},
    "india": {"wet": ("Wet", "leaf"), "dry": ("Dry", "recycle"), "sanitary": ("Sanitary", "drop"), "special": ("Special care", "warn")},
    "italy": {"organico": ("Organico", "leaf", "Umido: food scraps, soiled paper"), "carta": ("Carta", "paper", "Paper, cardboard, drink cartons"),
              "plastica": ("Plastica", "bottle", "Plastic packaging, cans, tins"), "vetro": ("Vetro", "jar", "Glass bottles and jars"),
              "secco": ("Secco", "trash", "Indifferenziato: the rest"), "pile": ("Battery box", "battery", "Pile esauste"),
              "farmaci": ("Pharmacy bin", "cross", "Farmaci scaduti"), "centro": ("Isola ecologica", "truck", "RAEE, paint, bulky, hazardous")},
    "norway": {"food": ("Food waste", "leaf", "Matavfall: scraps, bones, grounds"), "plastic": ("Plastic", "bottle", "Plastemballasje: bottles, bags, film"),
               "paper": ("Paper & cartons", "paper", "Papir, kartong, drikkekartong"), "glassmetal": ("Glass & metal", "jar", "Jars, bottles, tins, cans"),
               "rest": ("Residual", "flame", "Restavfall: burned for energy"), "station": ("Recycling station", "truck", "Hazardous, electrical, flat glass"),
               "pharmacy": ("Pharmacy", "cross", "Apotek: leftover medicines")},
    "spain": {"amarillo": ("Yellow", "recycle", "Envases: plastic, cans, cartons"), "azul": ("Blue", "paper", "Papel y cartón"),
              "verde": ("Green", "jar", "Vidrio: bottles and jars"), "marron": ("Brown", "leaf", "Orgánico: food, kitchen paper"),
              "resto": ("Grey", "trash", "Resto: everything else"), "puntolimpio": ("Punto limpio", "truck", "Hazardous, electrical, flat glass"),
              "sigre": ("SIGRE point", "cross", "Pharmacy: medicines")},
    "sweden": {"plastic": ("Plastic", "bottle", "Plastic packaging: bottles, bags, film"), "paper": ("Paper", "box", "Paper packaging: boxes, cartons"),
               "glass": ("Glass", "jar", "Glass packaging: bottles, jars"), "metal": ("Metal", "can", "Metal packaging: tins, lids"),
               "food": ("Food waste", "apple"), "general": ("General waste", "flame"), "centre": ("Recycling centre", "truck")},
    "usa": {"recycling": ("Recycling", "recycle"), "trash": ("Trash", "trash"), "compost": ("Compost", "leaf", "Food and yard waste, if offered"),
            "hhw": ("Hazardous drop-off", "warn"), "takeback": ("Drug take-back", "cross", "Pharmacy: unused medicines"),
            "storebag": ("Store drop-off", "bag", "Plastic bags and film")},
}


def glyph(b):
    text = f"{b['id']} {b['label']} {b.get('sub', '')}".lower()
    for key, g in GLYPHS:
        if key in text:
            return g
    return "recycle"


def main():
    regions = {}
    for path in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        key = os.path.splitext(os.path.basename(path))[0]
        d = json.load(open(path))
        ids = {b["id"] for b in d["bins"]}
        bins = []
        for i, b in enumerate(d["bins"]):
            o = OVERRIDES.get(key, {}).get(b["id"], ())
            bins.append({"id": b["id"], "label": o[0] if o else b["label"], "sub": o[2] if len(o) > 2 else b.get("sub", ""),
                         "c": b["colour"], "divert": bool(b.get("divert", True)),
                         "g": o[1] if o else glyph(b), "pat": PATS[i % len(PATS)]})
        items = {}
        for iid in ITEM_IDS:
            it = d["items"].get(iid)
            if not it or not it.get("a"):
                continue
            bad = [a for a in it["a"] if a not in ids]
            if bad:
                sys.exit(f"{key}/{iid}: unknown bin {bad}")
            items[iid] = {"a": it["a"], "w": it["w"], "v": bool(it.get("v"))}
        regions[key] = {"name": d["name"], "sub": d["sub"], "bins": bins, "items": items}
        print(f"{d['name']:10} {len(bins)} bins, {len(items)} items: " + ", ".join(f"{b['label']}[{b['g']}]" for b in bins))
    s = open(PAGE).read()
    s = re.sub(r"/\*REGIONS\*/.*?/\*END\*/", lambda m: "/*REGIONS*/" + json.dumps(regions, ensure_ascii=False) + "/*END*/", s, flags=re.S)
    open(PAGE, "w").write(s)


main()
