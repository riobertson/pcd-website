#!/usr/bin/env python3
"""Build the printable HTML worksheets for the 12-phase Sunday school curriculum.

Run from anywhere:  python3 build_printables.py
Outputs (next to this script):
  phase-01-printables.html … phase-12-printables.html
  bible-passport.html, certificate.html, index.html

Each phase file contains: a book-name coloring page (bubble letters), a
symbol coloring page, a Little Lambs tracing sheet, a spelling practice
sheet, a word search (+ answer key), a word scramble (+ answer key) and
cut-out flashcards. Open in a browser and print (Letter, portrait).
"""
import html
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent

SECTION_COLORS = {
    "Law": "#e53935",
    "History": "#fb8c00",
    "Poetry & Wisdom": "#fdd835",
    "Major Prophets": "#43a047",
    "Minor Prophets": "#4fc3f7",
    "Gospels": "#8e24aa",
    "History (NT)": "#795548",
    "Paul's Letters": "#1e3a8a",
    "General Letters": "#9e9e9e",
    "Prophecy": "#d4a017",
}

# (book, syllables, section)
BOOKS = [
    ("Genesis", "Gen·e·sis", "Law"), ("Exodus", "Ex·o·dus", "Law"),
    ("Leviticus", "Le·vit·i·cus", "Law"), ("Numbers", "Num·bers", "Law"),
    ("Deuteronomy", "Deu·ter·on·o·my", "Law"),
    ("Joshua", "Josh·u·a", "History"), ("Judges", "Judg·es", "History"),
    ("Ruth", "Ruth", "History"), ("1 Samuel", "Sam·u·el", "History"),
    ("2 Samuel", "Sam·u·el", "History"), ("1 Kings", "Kings", "History"),
    ("2 Kings", "Kings", "History"), ("1 Chronicles", "Chron·i·cles", "History"),
    ("2 Chronicles", "Chron·i·cles", "History"), ("Ezra", "Ez·ra", "History"),
    ("Nehemiah", "Ne·he·mi·ah", "History"), ("Esther", "Es·ther", "History"),
    ("Job", "Job", "Poetry & Wisdom"), ("Psalms", "Psalms", "Poetry & Wisdom"),
    ("Proverbs", "Prov·erbs", "Poetry & Wisdom"),
    ("Ecclesiastes", "Ec·cle·si·as·tes", "Poetry & Wisdom"),
    ("Song of Songs", "Song of Songs", "Poetry & Wisdom"),
    ("Isaiah", "I·sai·ah", "Major Prophets"), ("Jeremiah", "Jer·e·mi·ah", "Major Prophets"),
    ("Lamentations", "Lam·en·ta·tions", "Major Prophets"),
    ("Ezekiel", "E·ze·ki·el", "Major Prophets"), ("Daniel", "Dan·iel", "Major Prophets"),
    ("Hosea", "Ho·se·a", "Minor Prophets"), ("Joel", "Jo·el", "Minor Prophets"),
    ("Amos", "A·mos", "Minor Prophets"), ("Obadiah", "O·ba·di·ah", "Minor Prophets"),
    ("Jonah", "Jo·nah", "Minor Prophets"), ("Micah", "Mi·cah", "Minor Prophets"),
    ("Nahum", "Na·hum", "Minor Prophets"), ("Habakkuk", "Ha·bak·kuk", "Minor Prophets"),
    ("Zephaniah", "Zeph·a·ni·ah", "Minor Prophets"), ("Haggai", "Hag·gai", "Minor Prophets"),
    ("Zechariah", "Zech·a·ri·ah", "Minor Prophets"), ("Malachi", "Mal·a·chi", "Minor Prophets"),
    ("Matthew", "Mat·thew", "Gospels"), ("Mark", "Mark", "Gospels"),
    ("Luke", "Luke", "Gospels"), ("John", "John", "Gospels"),
    ("Acts", "Acts", "History (NT)"),
    ("Romans", "Ro·mans", "Paul's Letters"), ("1 Corinthians", "Co·rin·thi·ans", "Paul's Letters"),
    ("2 Corinthians", "Co·rin·thi·ans", "Paul's Letters"), ("Galatians", "Ga·la·tians", "Paul's Letters"),
    ("Ephesians", "E·phe·sians", "Paul's Letters"), ("Philippians", "Phi·lip·pi·ans", "Paul's Letters"),
    ("Colossians", "Co·los·sians", "Paul's Letters"),
    ("1 Thessalonians", "Thes·sa·lo·ni·ans", "Paul's Letters"),
    ("2 Thessalonians", "Thes·sa·lo·ni·ans", "Paul's Letters"),
    ("1 Timothy", "Tim·o·thy", "Paul's Letters"), ("2 Timothy", "Tim·o·thy", "Paul's Letters"),
    ("Titus", "Ti·tus", "Paul's Letters"), ("Philemon", "Phi·le·mon", "Paul's Letters"),
    ("Hebrews", "He·brews", "General Letters"), ("James", "James", "General Letters"),
    ("1 Peter", "Pe·ter", "General Letters"), ("2 Peter", "Pe·ter", "General Letters"),
    ("1 John", "John", "General Letters"), ("2 John", "John", "General Letters"),
    ("3 John", "John", "General Letters"), ("Jude", "Jude", "General Letters"),
    ("Revelation", "Rev·e·la·tion", "Prophecy"),
]
BOOK_INDEX = {b[0]: i for i, b in enumerate(BOOKS)}

PHASES = [
    dict(n=1, slug="in-the-beginning", title="In the Beginning", first="Genesis", last="Genesis",
         verse="In the beginning God created the heavens and the earth.", ref="Genesis 1:1",
         symbol="sun",
         words=["CREATION", "ADAM", "EVE", "NOAH", "ARK", "RAINBOW", "ABRAHAM", "JOSEPH", "PROMISE", "GARDEN"]),
    dict(n=2, slug="freedom-and-gods-good-rules", title="Freedom & God's Good Rules", first="Exodus", last="Deuteronomy",
         verse="Love the LORD your God with all your heart and with all your soul and with all your strength.", ref="Deuteronomy 6:5",
         symbol="tablets",
         words=["MOSES", "PLAGUES", "PASSOVER", "MANNA", "SINAI", "TABERNACLE", "WILDERNESS", "LAW"]),
    dict(n=3, slug="into-the-promised-land", title="Into the Promised Land", first="Joshua", last="Ruth",
         verse="Be strong and courageous… for the LORD your God will be with you wherever you go.", ref="Joshua 1:9",
         symbol="walls",
         words=["JERICHO", "RAHAB", "GIDEON", "DEBORAH", "SAMSON", "NAOMI", "BOAZ", "JORDAN"]),
    dict(n=4, slug="kings-and-kingdoms", title="Kings & Kingdoms", first="1 Samuel", last="2 Chronicles",
         verse="People look at the outward appearance, but the LORD looks at the heart.", ref="1 Samuel 16:7",
         symbol="crown",
         words=["HANNAH", "DAVID", "GOLIATH", "SAUL", "SOLOMON", "TEMPLE", "ELIJAH", "ELISHA"]),
    dict(n=5, slug="coming-home-and-being-brave", title="Coming Home & Being Brave", first="Ezra", last="Esther",
         verse="Do not grieve, for the joy of the LORD is your strength.", ref="Nehemiah 8:10",
         symbol="wall",
         words=["JERUSALEM", "WALLS", "QUEEN", "MORDECAI", "BRAVE", "EXILE", "REBUILD", "PURIM"]),
    dict(n=6, slug="songs-and-wise-words", title="Songs & Wise Words", first="Job", last="Song of Songs",
         verse="Your word is a lamp for my feet, a light on my path.", ref="Psalm 119:105",
         symbol="harp",
         words=["SHEPHERD", "WISDOM", "PRAISE", "HARP", "PATIENCE", "PRAYER", "SONG"]),
    dict(n=7, slug="gods-big-messengers", title="God's Big Messengers", first="Isaiah", last="Daniel",
         verse="The grass withers and the flowers fall, but the word of our God endures forever.", ref="Isaiah 40:8",
         symbol="scroll",
         words=["MESSIAH", "LIONS", "FURNACE", "POTTER", "BONES", "HOPE", "SCROLL"]),
    dict(n=8, slug="twelve-mighty-messengers", title="Twelve Mighty Messengers", first="Hosea", last="Malachi",
         verse="Act justly and … love mercy and … walk humbly with your God.", ref="Micah 6:8",
         symbol="fish",
         words=["NINEVEH", "FISH", "BETHLEHEM", "MERCY", "PROPHET", "JUSTICE"]),
    dict(n=9, slug="meet-jesus", title="Meet Jesus!", first="Matthew", last="John",
         verse="For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.", ref="John 3:16",
         symbol="cross",
         words=["JESUS", "MIRACLE", "PARABLE", "DISCIPLES", "CROSS", "RISEN", "MANGER", "GOSPEL"]),
    dict(n=10, slug="the-church-is-born", title="The Church Is Born", first="Acts", last="Acts",
         verse="You will receive power when the Holy Spirit comes on you; and you will be my witnesses.", ref="Acts 1:8",
         symbol="flame",
         words=["PENTECOST", "SPIRIT", "PETER", "PAUL", "CHURCH", "JOURNEY", "SHIPWRECK", "DAMASCUS"]),
    dict(n=11, slug="letters-from-paul", title="Letters from Paul", first="Romans", last="Philemon",
         verse="For it is by grace you have been saved, through faith… it is the gift of God.", ref="Ephesians 2:8",
         symbol="letter",
         words=["GRACE", "FAITH", "LOVE", "ARMOR", "JOY", "FRUIT"]),
    dict(n=12, slug="faith-hope-and-forever", title="Faith, Hope & Forever", first="Hebrews", last="Revelation",
         verse="Jesus Christ is the same yesterday and today and forever.", ref="Hebrews 13:8",
         symbol="crownstar",
         words=["HOPE", "HEAVEN", "CROWN", "ALPHA", "OMEGA", "PATMOS", "FOREVER"]),
]


def phase_books(p):
    return BOOKS[BOOK_INDEX[p["first"]]: BOOK_INDEX[p["last"]] + 1]


# ---------------------------------------------------------------- symbols
# Simple outline drawings for kids to color (black stroke, white fill).
S = 'fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
SYMBOLS = {
    "sun": f'''<circle cx="200" cy="200" r="70" {S}/>
      {''.join(f'<line x1="{200+95*c:.0f}" y1="{200+95*s:.0f}" x2="{200+140*c:.0f}" y2="{200+140*s:.0f}" {S}/>'
               for c, s in [(1,0),(0.707,0.707),(0,1),(-0.707,0.707),(-1,0),(-0.707,-0.707),(0,-1),(0.707,-0.707)])}
      <circle cx="175" cy="185" r="8" {S}/><circle cx="225" cy="185" r="8" {S}/>
      <path d="M170 225 Q200 250 230 225" {S}/>''',
    "tablets": f'''<path d="M60 340 V120 Q60 60 120 60 Q180 60 180 120 V340 Z" {S}/>
      <path d="M220 340 V120 Q220 60 280 60 Q340 60 340 120 V340 Z" {S}/>
      {''.join(f'<text x="120" y="{140+i*45}" font-size="34" text-anchor="middle" font-family="Georgia" {S} stroke-width="2">{r}</text>' for i, r in enumerate(["I","II","III","IV","V"]))}
      {''.join(f'<text x="280" y="{140+i*45}" font-size="34" text-anchor="middle" font-family="Georgia" {S} stroke-width="2">{r}</text>' for i, r in enumerate(["VI","VII","VIII","IX","X"]))}''',
    "walls": f'''<rect x="40" y="200" width="320" height="140" {S}/>
      <rect x="60" y="120" width="70" height="80" {S}/><rect x="270" y="120" width="70" height="80" {S}/>
      {''.join(f'<rect x="{60+i*23}" y="100" width="14" height="20" {S}/>' for i in range(3))}
      {''.join(f'<rect x="{270+i*23}" y="100" width="14" height="20" {S}/>' for i in range(3))}
      <path d="M170 340 V270 Q200 240 230 270 V340" {S}/>
      {''.join(f'<line x1="40" y1="{240+i*35}" x2="360" y2="{240+i*35}" {S} stroke-width="2"/>' for i in range(3))}
      <path d="M200 60 L200 20 M200 20 Q230 30 250 20 Q230 40 200 40" {S}/>''',
    "crown": f'''<path d="M60 300 L60 140 L130 210 L200 100 L270 210 L340 140 L340 300 Z" {S}/>
      <rect x="55" y="300" width="290" height="40" {S}/>
      <circle cx="200" cy="90" r="16" {S}/><circle cx="60" cy="130" r="14" {S}/><circle cx="340" cy="130" r="14" {S}/>
      <circle cx="130" cy="260" r="16" {S}/><circle cx="200" cy="250" r="20" {S}/><circle cx="270" cy="260" r="16" {S}/>''',
    "wall": f'''{''.join(f'<rect x="{30+(i%5)*70+(35 if (i//5)%2 else 0)}" y="{150+(i//5)*50}" width="70" height="50" {S}/>' for i in range(20) if 30+(i%5)*70+(35 if (i//5)%2 else 0) < 340)}
      <path d="M70 140 L110 60 L150 140" {S}/><circle cx="110" cy="45" r="15" {S}/>
      <path d="M250 140 L250 70 L300 70" {S}/><circle cx="310" cy="60" r="18" {S}/>''',
    "harp": f'''<path d="M100 340 L100 80 Q220 40 300 160 Q320 260 300 340 Z" {S}/>
      {''.join(f'<line x1="{120+i*30}" y1="{90+i*8}" x2="{120+i*30}" y2="330" {S} stroke-width="2"/>' for i in range(6))}
      <path d="M320 70 l10 20 l20 3 l-15 14 l4 20 l-19 -10 l-19 10 l4 -20 l-15 -14 l20 -3 z" {S}/>''',
    "scroll": f'''<rect x="90" y="90" width="220" height="220" {S}/>
      <rect x="60" y="70" width="30" height="260" rx="15" {S}/><rect x="310" y="70" width="30" height="260" rx="15" {S}/>
      {''.join(f'<line x1="115" y1="{130+i*35}" x2="285" y2="{130+i*35}" {S} stroke-width="2"/>' for i in range(5))}''',
    "fish": f'''<path d="M60 200 Q180 60 300 200 Q180 340 60 200 Z" {S}/>
      <path d="M300 200 L360 140 L360 260 Z" {S}/><circle cx="120" cy="185" r="12" {S}/>
      <path d="M170 150 Q190 200 170 250 M210 140 Q230 200 210 260" {S}/>
      <circle cx="90" cy="90" r="10" {S}/><circle cx="70" cy="60" r="7" {S}/><circle cx="100" cy="40" r="5" {S}/>''',
    "cross": f'''<path d="M170 40 H230 V130 H310 V190 H230 V360 H170 V190 H90 V130 H170 Z" {S}/>
      <path d="M40 360 Q200 300 360 360" {S}/>
      {''.join(f'<line x1="{200+60*c:.0f}" y1="{160+60*s:.0f}" x2="{200+150*c:.0f}" y2="{160+150*s:.0f}" {S} stroke-width="2"/>' for c, s in [(0.5,-0.87),(-0.5,-0.87),(0.87,-0.5),(-0.87,-0.5)])}''',
    "flame": f'''<path d="M200 340 Q90 300 120 190 Q140 230 160 220 Q140 130 210 60 Q210 150 260 170 Q270 130 260 110 Q340 200 290 290 Q260 340 200 340 Z" {S}/>
      <path d="M200 320 Q150 290 175 230 Q195 260 205 250 Q200 200 230 180 Q250 260 240 300 Q225 320 200 320 Z" {S}/>''',
    "letter": f'''<rect x="50" y="110" width="300" height="200" {S}/>
      <path d="M50 110 L200 220 L350 110" {S}/><path d="M50 310 L160 200 M350 310 L240 200" {S}/>
      <path d="M300 40 Q340 60 320 100 L270 150 L260 140 L310 90 Q320 70 300 60 Z" {S}/>''',
    "crownstar": f'''<path d="M200 40 l25 55 l60 6 l-45 40 l14 59 l-54 -32 l-54 32 l14 -59 l-45 -40 l60 -6 z" {S}/>
      <path d="M80 340 L80 250 L140 290 L200 230 L260 290 L320 250 L320 340 Z" {S}/>
      <circle cx="140" cy="320" r="10" {S}/><circle cx="200" cy="315" r="12" {S}/><circle cx="260" cy="320" r="10" {S}/>''',
}

CSS = """
@page { size: letter portrait; margin: 0.5in; }
* { box-sizing: border-box; }
body { font-family: "Comic Sans MS", "Chalkboard SE", "Trebuchet MS", sans-serif; color: #000; background: #fff; margin: 0; }
.sheet { page-break-after: always; break-after: page; min-height: 9.5in; padding: 0.2in; position: relative; }
.sheet:last-child { page-break-after: auto; break-after: auto; }
h1 { font-size: 26pt; text-align: center; margin: 0 0 4px; }
h2 { font-size: 16pt; text-align: center; margin: 0 0 12px; font-weight: normal; }
.namebar { font-size: 13pt; margin-bottom: 14px; display: flex; justify-content: space-between; }
.verse { text-align: center; font-size: 15pt; margin-top: 14px; border: 3px dashed #000; padding: 10px; border-radius: 12px; }
.footer { position: absolute; bottom: 0.1in; left: 0; right: 0; text-align: center; font-size: 9pt; color: #555; }
svg { display: block; margin: 0 auto; }
.grid { border-collapse: collapse; margin: 0 auto; }
.grid td { width: 0.42in; height: 0.42in; text-align: center; font-size: 15pt; font-family: "Courier New", monospace; font-weight: bold; border: 1px solid #bbb; }
.grid td.hit { background: #ffeb3b; }
.wordlist { columns: 3; font-size: 13pt; margin: 18px auto 0; max-width: 7in; }
.wordlist div { padding: 2px 0; }
.scramble { font-size: 15pt; line-height: 2.1; max-width: 7in; margin: 0 auto; }
.scramble td { padding: 6px 8px; }
.scramble .q { font-family: "Courier New", monospace; font-weight: bold; letter-spacing: 3px; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.card { border: 2px dashed #777; height: 2.1in; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; overflow: hidden; }
.card .band { position: absolute; top: 0; left: 0; right: 0; height: 0.35in; color: #fff; font-size: 10pt; display: flex; align-items: center; justify-content: center; font-weight: bold; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.card .name { font-size: 26pt; font-weight: bold; margin-top: 0.2in; text-align: center; }
.card .syl { font-size: 14pt; color: #333; }
.card .num { position: absolute; bottom: 6px; right: 10px; font-size: 10pt; color: #555; }
.spell { width: 100%; border-collapse: collapse; font-size: 14pt; }
.spell td { border-bottom: 2px solid #000; height: 0.62in; vertical-align: bottom; padding: 2px 6px; }
.spell td.word { font-weight: bold; width: 2.3in; border-bottom: none; }
.spell td.claps { width: 1.1in; border-bottom: none; font-size: 11pt; color: #444; }
.key { font-size: 11pt; color: #444; text-align: center; margin-top: 6px; }
.tip { font-size: 11pt; color: #333; text-align: center; margin: 4px 0 10px; }
@media screen { body { background: #ddd; } .sheet { background: #fff; width: 8.5in; margin: 0.25in auto; padding: 0.5in; box-shadow: 0 2px 8px rgba(0,0,0,.3); min-height: 11in; } .noprint { text-align:center; padding: 10px; font-family: sans-serif; } }
@media print { .noprint { display: none; } }
"""


def page(title, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head>
<body>
<div class="noprint">🖨️ Print this page (Letter, portrait). Each worksheet prints on its own page. Turn on "Background graphics" for colored flashcard bands.</div>
{body}
</body></html>
"""


NAMEBAR = '<div class="namebar"><span>Name: ______________________</span><span>Date: ____________</span></div>'


def footer(p):
    return f'<div class="footer">Purpose Church Kids · Through the Bible in 12 Months · Phase {p["n"]}: {html.escape(p["title"])}</div>'


def bubble_text_svg(lines, width=720, max_size=96, dashed=False):
    """Outlined (colorable) letters. dashed=True makes dotted tracing letters."""
    rows = []
    h = 0
    for line in lines:
        size = min(max_size, int(width / max(len(line), 1) * 1.55))
        h += size * 1.25
        rows.append((line, size, h - size * 0.3))
    extra = 'stroke-dasharray="3 6"' if dashed else ""
    texts = "".join(
        f'<text x="{width/2}" y="{y:.0f}" font-size="{s}" text-anchor="middle" '
        f'font-family="Arial Rounded MT Bold, Arial Black, Verdana, sans-serif" font-weight="900" '
        f'fill="#fff" stroke="#000" stroke-width="{3 if not dashed else 2.5}" {extra} '
        f'stroke-linejoin="round" paint-order="stroke">{html.escape(t)}</text>'
        for t, s, y in rows)
    return f'<svg width="100%" viewBox="0 0 {width} {h + 10:.0f}" xmlns="http://www.w3.org/2000/svg">{texts}</svg>'


def coloring_names(p, books):
    names = [b[0] for b in books]
    section = ", ".join(dict.fromkeys(b[2] for b in books))
    total = BOOK_INDEX[p["last"]] + 1
    if len(names) <= 5:
        art = bubble_text_svg(names, max_size=170 if len(names) == 1 else 110)
    else:
        cells = "".join(f'<div>{bubble_text_svg([n], width=360, max_size=64)}</div>' for n in names)
        art = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 18px">{cells}</div>'
    return f"""<section class="sheet">{NAMEBAR}
<h1>Phase {p["n"]}: {html.escape(p["title"])}</h1>
<h2>Color the books of the Bible! · {html.escape(section)}</h2>
{art}
<div class="verse">"{html.escape(p["verse"])}" · {html.escape(p["ref"])}</div>
<div class="tip">I know <b>{total}</b> of 66 books! ⭐ Color one star for each time you sing the song: ☆ ☆ ☆ ☆ ☆</div>
{footer(p)}</section>"""


def coloring_symbol(p):
    return f"""<section class="sheet">{NAMEBAR}
<h1>{html.escape(p["title"])}</h1>
<h2>Color the picture and draw your favorite story from this month around it.</h2>
<svg width="85%" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{SYMBOLS[p["symbol"]]}</svg>
{bubble_text_svg([p["ref"]], max_size=60)}
<div class="verse">"{html.escape(p["verse"])}"</div>
{footer(p)}</section>"""


def tracing(p, books):
    def row(b):
        first = b[0].lstrip("123 ")[0]
        return (f'<div style="display:flex;align-items:center;gap:14px;margin:4px 0">'
                f'<svg width="1in" viewBox="0 0 100 100"><text x="50" y="82" font-size="90" text-anchor="middle" '
                f'font-family="Arial Black, sans-serif" fill="#fff" stroke="#000" stroke-width="3">{first}</text></svg>'
                f'<div style="flex:1">{bubble_text_svg([b[0]], width=560, max_size=64, dashed=True)}</div></div>')
    if len(books) < 3:
        books = (books * 6)[:6]  # one-book phases: repeat for extra tracing practice
    sheets = []
    for i in range(0, len(books), 6):
        sheets.append(f"""<section class="sheet">{NAMEBAR}
<h1>🐑 Little Lambs Tracing</h1>
<h2>Color the big first letter. Say its sound. Trace the dotted book name with your finger, then a crayon!</h2>
{''.join(row(b) for b in books[i:i+6])}
{footer(p)}</section>""")
    return "".join(sheets)


def spelling(p, books):
    seen, rows = set(), []
    for name, syl, _ in books:
        if name in seen:
            continue
        seen.add(name)
        claps = len(syl.split("·")) if "·" in syl else len(syl.split())
        rows.append(f'<tr><td class="word">{html.escape(name)}<br><span style="font-weight:normal;font-size:11pt">{html.escape(syl)}</span></td>'
                    f'<td class="claps">👏 × {claps}</td><td></td><td></td></tr>')
    for w in p["words"]:
        if len(rows) % 9 == 0 and len(rows) >= 9:
            break
        rows.append(f'<tr><td class="word">{html.escape(w.title())}<br><span style="font-weight:normal;font-size:11pt">⭐ bonus word</span></td>'
                    f'<td class="claps">👏</td><td></td><td></td></tr>')
    sheets = []
    for i in range(0, len(rows), 9):
        sheets.append(f"""<section class="sheet">{NAMEBAR}
<h1>🔤 Spelling Practice</h1>
<h2>Look · Say · Clap · Cover · Write · Check</h2>
<table class="spell"><tr><td class="word"></td><td class="claps"><b>Claps</b></td><td><b>Write it</b></td><td><b>Write it again</b></td></tr>
{''.join(rows[i:i+9])}</table>
<div class="tip">Explorers & up: Can you spell them with your eyes closed? Trailblazers & Ambassadors: Write ALL the books you know so far on the back, in order!</div>
{footer(p)}</section>""")
    return "".join(sheets)


def clean(word):
    return "".join(ch for ch in word.upper() if ch.isalpha())


def make_wordsearch(words, size, seed):
    rnd = random.Random(seed)
    dirs = [(0, 1), (1, 0), (1, 1)]  # right, down, diagonal (no backwards: kid-friendly)
    for _attempt in range(200):
        grid = [[None] * size for _ in range(size)]
        placed = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            spots = []
            for dr, dc in dirs:
                for r in range(size):
                    for c in range(size):
                        er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                        if er >= size or ec >= size:
                            continue
                        cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
                        if all(grid[a][b] in (None, w[i]) for i, (a, b) in enumerate(cells)):
                            spots.append(cells)
            if not spots:
                ok = False
                break
            cells = rnd.choice(spots)
            for i, (a, b) in enumerate(cells):
                grid[a][b] = w[i]
            placed[w] = cells
        if ok:
            letters = "ABCDEFGHIJKLMNOPRSTUVWY"
            for r in range(size):
                for c in range(size):
                    if grid[r][c] is None:
                        grid[r][c] = rnd.choice(letters)
            return grid, placed
    raise RuntimeError("could not build word search")


def wordsearch(p, books):
    words = list(dict.fromkeys(clean(b[0]) for b in books))
    for w in p["words"]:
        if clean(w) not in words and len(words) < 16:
            words.append(clean(w))
    size = max(13, max(len(w) for w in words) + 1)
    grid, placed = make_wordsearch(words, size, seed=p["n"] * 7919)
    hits = {cell for cells in placed.values() for cell in cells}

    def table(show):
        return '<table class="grid">' + "".join(
            "<tr>" + "".join(f'<td class="{"hit" if show and (r, c) in hits else ""}">{grid[r][c]}</td>'
                             for c in range(size)) + "</tr>" for r in range(size)) + "</table>"

    wl = "".join(f"<div>☐ {w}</div>" for w in words)
    note = "Words go → across, ↓ down, or ↘ diagonal. Numbers like “1” and “2” are left out."
    return f"""<section class="sheet">{NAMEBAR}
<h1>🔎 Word Search</h1><h2>Phase {p["n"]}: {html.escape(p["title"])}</h2>
<div class="tip">{note}</div>
{table(False)}<div class="wordlist">{wl}</div>
{footer(p)}</section>
<section class="sheet"><h1>Answer Key: Word Search</h1><h2>Teacher copy</h2>
{table(True)}{footer(p)}</section>"""


def scramble(p, books):
    rnd = random.Random(p["n"] * 104729)
    items = list(dict.fromkeys([b[0] for b in books] + [w.title() for w in p["words"]]))[:12]
    rows, keys = [], []
    for i, word in enumerate(items, 1):
        letters = list(clean(word))
        for _ in range(20):
            rnd.shuffle(letters)
            if "".join(letters) != clean(word) or len(letters) < 3:
                break
        hint = "📖 book" if word in BOOK_INDEX else "💡 word"
        rows.append(f'<tr><td>{i}.</td><td class="q">{"".join(letters)}</td><td>{hint}</td><td>______________________</td></tr>')
        keys.append(f"{i}. {html.escape(word)}")
    return f"""<section class="sheet">{NAMEBAR}
<h1>🌀 Word Scramble</h1><h2>Unscramble the books and words from Phase {p["n"]}</h2>
<table class="scramble">{''.join(rows)}</table>
<div class="key" style="margin-top:30px;transform:rotate(180deg)">Answer key: {' · '.join(keys)}</div>
{footer(p)}</section>"""


def flashcards(p, books):
    cards = []
    for name, syl, sec in books:
        color = SECTION_COLORS[sec]
        txt = "#000" if sec in ("Poetry & Wisdom", "Minor Prophets") else "#fff"
        cards.append(f'<div class="card"><div class="band" style="background:{color};color:{txt}">{html.escape(sec)}</div>'
                     f'<div class="name">{html.escape(name)}</div><div class="syl">{html.escape(syl)}</div>'
                     f'<div class="num">Book #{BOOK_INDEX[name]+1} of 66</div></div>')
    sheets = []
    for i in range(0, len(cards), 8):
        sheets.append(f"""<section class="sheet"><h1 style="font-size:16pt">✂️ Flashcards: Phase {p["n"]}</h1>
<div class="cards">{''.join(cards[i:i+8])}</div>{footer(p)}</section>""")
    return "".join(sheets)


def build_phase(p):
    books = phase_books(p)
    body = "".join([
        coloring_names(p, books), coloring_symbol(p), tracing(p, books), spelling(p, books),
        wordsearch(p, books), scramble(p, books), flashcards(p, books),
    ])
    out = OUT / f"phase-{p['n']:02d}-printables.html"
    out.write_text(page(f"Phase {p['n']} Printables", body), encoding="utf-8")
    return out


def build_passport():
    stamps = "".join(
        f'<div style="border:3px solid #000;border-radius:14px;height:2in;padding:8px;text-align:center;position:relative">'
        f'<div style="font-weight:bold">Phase {p["n"]}</div><div style="font-size:11pt">{html.escape(p["title"])}</div>'
        f'<div style="font-size:9pt;color:#444">{html.escape(p["first"] + ("" if p["first"] == p["last"] else " – " + p["last"]))}</div>'
        f'<div style="position:absolute;bottom:6px;left:0;right:0;font-size:9pt;color:#666">stamp here · date ______</div></div>'
        for p in PHASES)
    body = f"""<section class="sheet" style="text-align:center">
<h1 style="font-size:40pt;margin-top:1in">🛂 MY BIBLE PASSPORT</h1>
<h2>Through the Bible in 12 Months · Purpose Church Kids</h2>
<svg width="45%" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{SYMBOLS["scroll"]}</svg>
<p style="font-size:16pt">Traveler's name: ______________________________</p>
<p style="font-size:16pt">Age: ______ &nbsp; Group: 🐑 Little Lambs · 🧭 Explorers · 🥾 Trailblazers · 🕊️ Ambassadors</p>
<p style="font-size:13pt">"Your word is a lamp for my feet, a light on my path." (Psalm 119:105)</p>
</section>
<section class="sheet"><h1>Passport Stamps</h1><h2>Earn a stamp when you finish each phase!</h2>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">{stamps}</div>
<p class="tip">When all 12 stamps are filled, you have traveled through all 66 books of the Bible! 🎉</p></section>"""
    (OUT / "bible-passport.html").write_text(page("Bible Passport", body), encoding="utf-8")


def build_certificate():
    body = """<section class="sheet" style="border:12px double #000;text-align:center;padding-top:1in">
<h1 style="font-size:38pt">Certificate of Completion</h1>
<h2>Through the Bible in 12 Months</h2>
<p style="font-size:16pt;margin-top:.5in">This certifies that</p>
<p style="font-size:28pt;border-bottom:2px solid #000;width:70%;margin:0 auto">&nbsp;</p>
<p style="font-size:16pt;margin-top:.3in">has traveled through all <b>66 books of the Bible</b>,<br>from Genesis to Revelation,<br>and is hereby named a</p>
<p style="font-size:26pt;font-weight:bold">☐ Bible Explorer &nbsp; ☐ 66 Books Champion &nbsp; ☐ Bible Ambassador</p>
<p style="font-size:14pt">"Your word is a lamp for my feet, a light on my path." (Psalm 119:105)</p>
<div style="display:flex;justify-content:space-around;margin-top:.8in;font-size:13pt">
<div>______________________<br>Teacher</div><div>______________________<br>Pastor</div><div>______________________<br>Date</div></div>
<p style="margin-top:.4in;font-size:12pt">Purpose Church Kids &amp; Youth Ministry</p>
</section>"""
    (OUT / "certificate.html").write_text(page("Certificate", body), encoding="utf-8")


def build_index():
    rows = "".join(
        f'<li><a href="phase-{p["n"]:02d}-printables.html">Phase {p["n"]}: {html.escape(p["title"])}</a> '
        f'({html.escape(p["first"] + ("" if p["first"] == p["last"] else " – " + p["last"]))})</li>' for p in PHASES)
    body = f"""<section class="sheet"><h1>📁 Printables</h1>
<h2>Through the Bible in 12 Months · Purpose Church Kids</h2>
<p>Each phase file contains: book-name coloring page, picture coloring page, Little Lambs tracing sheet,
spelling practice sheet, word search (+ answer key), word scramble (+ answer key), and cut-out flashcards.</p>
<ol style="font-size:15pt;line-height:1.8">{rows}</ol>
<p style="font-size:15pt">⭐ <a href="bible-passport.html">Bible Passport</a> · 🎓 <a href="certificate.html">Graduation Certificate</a></p>
</section>"""
    (OUT / "index.html").write_text(page("Curriculum Printables", body), encoding="utf-8")


if __name__ == "__main__":
    for p in PHASES:
        print("wrote", build_phase(p).name)
    build_passport()
    build_certificate()
    build_index()
    print("wrote bible-passport.html, certificate.html, index.html")
