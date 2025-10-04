import re
from pathlib import Path


def PatchColors():
    allFiles = []
    for p in Path("./").rglob("*.chopro"):
        allFiles.append(p)
    for p in Path("./").rglob("*.cho"):
        allFiles.append(p)

    onsongColor = re.compile(r"&blue:?")

    for p in allFiles:
        try:
            with open(p, mode="r", encoding="utf-8") as f:
                srcLines = f.readlines()

            addColor = False
            with open(p, mode="w", encoding="utf-8") as f:
                for line in srcLines:
                    if not addColor and onsongColor.search(line):
                        addColor = True
                        f.write("{textcolour: blue}\n")
                    elif addColor and not onsongColor.search(line):
                        addColor = False
                        f.write("{textcolour}\n")

                    if addColor:
                        newL = re.sub(".?&blue:?/? *", "", line)
                        f.write(newL)
                    else:
                        f.write(line)

                if addColor:
                    f.write("{textcolour}\n")

        except Exception as e:
            print(f"failed on file {str(p)}: {e}")
