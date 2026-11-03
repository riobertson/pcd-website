#!/usr/bin/env python3
"""Insert the "2nd & 4th Sunday Plan" section into every phase file.

Classes meet on the 2nd and 4th Sundays of each month, so each phase's four
lesson units are taught in pairs: Units 1+2 on the 2nd Sunday, Units 3+4 (plus
the end-of-phase review) on the 4th Sunday. The section is generated from each
phase's "Month at a Glance" table and is safe to re-run (it replaces itself).
"""
import re
from pathlib import Path

PHASES = Path(__file__).resolve().parent.parent / "phases"
START, END = "<!-- sunday-plan:start -->", "<!-- sunday-plan:end -->"
NOTE_START, NOTE_END = "<!-- sunday-plan-note:start -->", "<!-- sunday-plan-note:end -->"

# 2027 dates, for a January start (phase n = month n).
DATES = [("Jan 10", "Jan 24"), ("Feb 14", "Feb 28"), ("Mar 14", "Mar 28"), ("Apr 11", "Apr 25"),
         ("May 9", "May 23"), ("Jun 13", "Jun 27"), ("Jul 11", "Jul 25"), ("Aug 8", "Aug 22"),
         ("Sep 12", "Sep 26"), ("Oct 10", "Oct 24"), ("Nov 14", "Nov 28"), ("Dec 12", "Dec 26")]
CAL_NOTES = {
    3: "⚠️ **Mar 28, 2027 is Easter Sunday.** If your class has an Easter lesson that day (Phase 9's \"He Is Alive!\" lesson fits well), send Lessons 3 & 4 (Judges and Ruth) home as a family reading week and hold the Phase 3 check-offs on Apr 11.",
    5: "⚠️ **May 9, 2027 is Mother's Day.** Add a quick \"thank-you card for Mom or a special lady\" to the Activity slot (Ruth & Naomi or Esther themes fit well).",
    11: "⚠️ **Nov 28, 2027 is Thanksgiving weekend.** Expect lower attendance; keep the review check-offs open on the next 2nd Sunday for anyone who missed.",
    12: "⚠️ **Dec 26, 2027 is the day after Christmas.** Many churches move this class to **Dec 19** (3rd Sunday) so the Bible Bowl and graduation get full attendance. Decide early and tell families.",
}


def clean(cell):
    return re.sub(r"\*+", "", cell).strip()


def glance_rows(text):
    block = text.split("## Month at a Glance", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in block.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [clean(c) for c in line.strip().strip("|").split("|")]
        if cells[0].lower().startswith("week"):
            continue
        rows.append(dict(week=cells[0], passage=cells[1], title=cells[2].strip('"'), key=cells[3],
                         video=cells[4].replace("📺", "").strip(), game=cells[5].replace("🎮", "").strip(),
                         activity=cells[6]))
    return rows


def first(option_list):
    return re.split(r";\s*| / ", option_list)[0].strip()


def build(n, text):
    rows = glance_rows(text)
    u = rows[:4]
    review = rows[4] if len(rows) > 4 else None
    d2, d4 = DATES[n - 1]
    review_title = review["title"] if review else "Review & Fun Sunday"
    final = n == 12

    def unit(i):
        r = u[i]
        return f'**Lesson {i+1}: "{r["title"]}"** ({r["passage"]})'

    lines = [START, "", "## 📅 2nd & 4th Sunday Plan", "",
             "Our class meets on the **2nd and 4th Sundays** of each month, so the four lessons below are taught **two at a time**. "
             "Each Sunday is still 75 minutes, with two shorter stories. Use the full lesson write-ups in **Weekly Lessons** for scripts, questions and supplies.",
             "",
             "| Sunday | 2027 date* | Teach | Big takeaway |",
             "|---|---|---|---|",
             f'| **2nd Sunday** | {d2} | {unit(0)} + {unit(1)} | {u[0]["key"]} {u[1]["key"]} |',
             f'| **4th Sunday** | {d4} | {unit(2)} + {unit(3)} + **{"Bible Bowl & Graduation" if final else "End-of-Phase Review"}** | {u[2]["key"]} {u[3]["key"]} |',
             "",
             "*\\*Dates assume a January 2027 start. See the [Program Overview](../00-start-here/program-overview.md#5-our-calendar-2nd--4th-sundays) for the full calendar.*",
             ""]
    if n in CAL_NOTES:
        lines += ["> " + CAL_NOTES[n], ""]

    def run_sheet(label, a, b, fourth):
        ra, rb = u[a], u[b]
        sheet = [f"### {label}: \"{ra['title']}\" + \"{rb['title']}\"", "",
                 "| Time | Segment | What to do |", "|---|---|---|"]
        recap = " Then a 2-minute recap: \"What do you remember from last time?\"" if fourth else ""
        sheet += [
            f"| 0:00–0:08 | 🎵 Welcome & Book Chant | Attendance, then sing this phase's book song with motions.{recap} |",
            f"| 0:08–0:20 | 📖 Story 1 | **{ra['title']}** ({ra['passage']}). Use the Lesson {a+1} hook and story script. Key point: *{ra['key']}* |",
            f"| 0:20–0:28 | 📺 Video | Show **one** video (Little Lambs & Explorers: Sharefaith Kids; Trailblazers & Ambassadors: BibleProject). Options: {ra['video']}. Send the others home on the family page. |",
            f"| 0:28–0:40 | 📖 Story 2 | **{rb['title']}** ({rb['passage']}). Use the Lesson {b+1} script. Key point: *{rb['key']}* |",
            f"| 0:40–0:48 | 💬 Small Groups | Ask 1 question from Lesson {a+1} and 1 from Lesson {b+1} for your age group, then: \"Where did we see Jesus today?\" |",
        ]
        if fourth and final:
            sheet += [
                "| 0:48–1:05 | 🏆 Bible Bowl (lightning round) | Play Rounds 1 and 2 of the Bible Bowl (20 questions) in mixed-age teams. Run the full 4-round Bible Bowl at your celebration event if you have one. |",
                "| 1:05–1:15 | 🎓 Passport, Badges & Prayer | Final check-offs, last Passport stamp, Forever Crown badge, certificates (or hand them out during the main service). Pray a blessing over the kids. |",
            ]
        elif fourth:
            sheet += [
                f"| 0:48–0:56 | 🎮 Game | **{first(ra['game'])}** (Lesson {a+1}). Backup: {first(rb['game'])}. |",
                f"| 0:56–1:04 | 🖍️ Activity | **{first(rb['activity'])}** (Lesson {b+1}). Early finishers: this phase's coloring page or word search. |",
                f"| 1:04–1:15 | ✅ Review, Passport & Prayer | Run the **End-of-Phase** oral check-offs by age group, stamp Bible Passports, hand out the phase badge, and pray. Anyone not finished can check off on the next 2nd Sunday. |",
            ]
        else:
            sheet += [
                f"| 0:48–0:58 | 🎮 Game | **{first(ra['game'])}** (Lesson {a+1}). Backup: {first(rb['game'])}. |",
                f"| 0:58–1:10 | 🖍️ Activity | **{first(rb['activity'])}** (Lesson {b+1}). Early finishers: this phase's coloring page or word search. |",
                "| 1:10–1:15 | ✅ Memory, Spelling & Prayer | Say the memory verse, spell 1–2 new books together, give stars, and pray. Send home the Take-Home Family Page. |",
            ]
        return sheet + [""]

    lines += run_sheet("2nd Sunday", 0, 1, False)
    lines += run_sheet("4th Sunday", 2, 3, True)
    if final:
        lines += ["> 🎓 **Graduation:** Use the short 10–15 minute graduation program from *End-of-Phase Review & Celebration* in the main worship service on the 4th Sunday, "
                  "or hold the full Bible Bowl & Graduation as a special event (for example, a Saturday afternoon or the 2nd Sunday of January as the next year's kickoff).", ""]

    lines += ["### 🏠 Between Sundays (the 1st and 3rd weeks)", "",
              "Kids go two weeks between classes, so the home weeks keep the memory work going. Put these on the family page or text them to parents:", "",
              f"- **After the 2nd Sunday:** Sing the book song once a day, practice this phase's spelling words (5 minutes), read or listen to {u[0]['passage']} and {u[1]['passage']} with a picture Bible, and watch the video the class didn't see.",
              f"- **After the 4th Sunday:** Read {u[3]['passage']} together, talk through the 3 dinner-table questions, and keep singing the whole song so far. " + ("Celebrate: your child now knows all 66 books!" if final else "The next phase starts on the 2nd Sunday!"),
              "- **Teachers:** A quick text or photo to parents mid-week (\"This week, practice spelling ___!\") makes a big difference.", "",
              "### ✂️ What to Trim When Time Is Short", "",
              "Two lessons in one Sunday means you **won't use everything** in the Weekly Lessons. Keep these, in this order: "
              "(1) both story scripts, (2) the memory verse and book song, (3) one game, (4) one activity. "
              "Extra games, crafts, trivia and puzzles become take-home pages, early-finisher options or fun for a 5th-Sunday or special event.", ""]
    if review:
        lines += [f"> 💡 **Optional bonus:** \"{review_title}\" (the old Week 5 review) can be used for a special event, a 5th Sunday if your church holds class, or folded into the 4th Sunday's review time.", ""]
    lines += ["---", "", END]
    return "\n".join(lines)


NOTE = (f"{NOTE_START}\n> 📅 **Twice a month:** The four lessons below are taught in pairs: **Lessons 1 & 2 on the 2nd Sunday**, "
        "**Lessons 3 & 4 on the 4th Sunday**. See the [2nd & 4th Sunday Plan](#-2nd--4th-sunday-plan) above for the 75-minute run sheets. "
        "\"Week 1–4\" below means Lesson 1–4.\n" + NOTE_END)

for path in sorted(PHASES.glob("phase-*.md")):
    n = int(path.name[6:8])
    text = path.read_text(encoding="utf-8")
    text = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n*", "", text, flags=re.S)
    text = re.sub(re.escape(NOTE_START) + r".*?" + re.escape(NOTE_END) + r"\n*", "", text, flags=re.S)
    section = build(n, text)
    text = re.sub(r"^## Weekly Lessons.*$", lambda m: section + "\n\n" + m.group(0) + "\n\n" + NOTE, text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")
    print("updated", path.name)
