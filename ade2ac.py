import json
import pathlib
import sys
import os
import shutil
import zipfile

import yaml

args = sys.argv

difficulty_colors = ["#3A6B78FF", "#566947FF", "#482B54FF", "#7C1C30FF"]
skins = ["light", "conflict", "colorless"]
colors = {
    "trace": "#9178AA7A",
    "shadow": "#5A5A5A5A",
    "arc": [
        '#0CD4D4D9',
        '#FF96DCD9',
        '#23FF6CD9'
    ],
    "arcLow": [
        '#19A0EBD9',
        '#F0699BD9',
        '#28C81ED9'
    ]
}

proj_path = args[1]

with open(f"{proj_path}/Arcade/Project.arcade", "r") as f:
    adeproj = json.load(f)

audio = input("Name of audio file: ")
preview_start = int(input("Start of preview: "))
preview_end = int(input("End of preview: "))
jacket = input("Name of jacket file: ")
illustrator = input("Illustrator of jacket: ")
bg_path = input("Path of background: ")
bpm_text = input("Text of BPM: ")
base_bpm = float(input(f"BaseBPM(Empty for: {adeproj['BaseBpm']}): ") or adeproj['BaseBpm'])
title = input(
    f"Name of the song(Empty for: \"{adeproj['Title']}\"): ") or adeproj['Title']
artist = input(
    f"Artist of the song(Empty for: \"{adeproj['Artist']}\"): ") or adeproj['Artist']
charter = input("Charter: ")
skin = int(input("Skin(0, 1 or 2): "))

diffs_num = list(
    map(int, input("Containing Difficulties(Format:\"0 1 2 3\"): ").split(" ")))
diffs = ["", "", "", ""]

for i in diffs_num:
    diff_text = str(adeproj['Difficulties'][i]['Rating'])
    diffs[i] = input(
        f"Text of difficulty {i}(Empty for:\"{diff_text}\")") or diff_text

print("Confirm informations:")
print(f"Title: {title}")
print(f"Artist: {artist}")
print(f"Audio: {audio}")
print(f"Preview: {preview_start}-{preview_end}")
print(f"Jacket: {jacket}")
print(f"Illustrator: {illustrator}")
print(f"Background: {bg_path}")
print(f"BaseBPM: {base_bpm}")
print(f"BPMText: {bpm_text}")
print(f"Skin: {skins[skin]}")
print("Difficulties:")
for i in diffs_num:
    print(f"  {i}: {diffs[i]}")
input("Enter to continue...")

arcproj = {
    "lastOpenedChartPath": "CreateByArcCreatePackageConvertor.aff",
    "charts": []
}

for i in diffs_num:
    arcproj["charts"].append({
        "chartPath": f"{i}.aff",
        "audioPath": audio,
        "jacketPath": jacket,
        "baseBpm": base_bpm,
        "bpmText": bpm_text,
        "syncBaseBpm": True,
        "backgroundPath": bg_path.replace("\\", "/").split("/")[-1],
        "title": title,
        "composer": artist,
        "charter": charter,
        "alias": "",
        "illustrator": illustrator,
        "difficulty": diffs[i],
        "difficultyColor": difficulty_colors[i],
        "skin": {
            "side": skins[skin],
            "singleLine": "none"
        },
        "colors": colors,
        "lastWorkingTiming": 0,
        "previewStart": preview_start,
        "previewEnd": preview_end
    })

package_name = input("Package name: ").lower()
select_identifier = input("Selection identifier: ").lower()
package_identifier = f"{select_identifier}.{package_name}"
print(f"Package identifier: {package_identifier}")

os.mkdir(f"./{package_name}")
os.mkdir(f"./{package_name}/{package_name}")
shutil.copy(pathlib.Path(proj_path) / audio,
            pathlib.Path(f"./{package_name}/{package_name}/"))
shutil.copy(pathlib.Path(proj_path) / jacket,
            pathlib.Path(f"./{package_name}/{package_name}/"))
shutil.copy(pathlib.Path(bg_path), pathlib.Path(
    f"./{package_name}/{package_name}/"))
for i in diffs_num:
    shutil.copy(pathlib.Path(proj_path) /
                f"{i}.aff", pathlib.Path(f"./{package_name}/{package_name}/"))

index = [{
    "directory": package_name,
    "identifier": package_identifier,
    "settingsFile": "project.arcproj",
    "type": "level"
}]

with open(f"./{package_name}/{package_name}/project.arcproj", "w") as f:
    yaml.dump(arcproj, f)

with open(f"./{package_name}/index.yml", "w") as f:
    yaml.dump(index, f)

def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()

zip_dir(f"./{package_name}", f"./{package_identifier}")

shutil.rmtree(f"./{package_name}")

print("Done!")
print(f"Output file: {pathlib.Path(f'./{package_identifier}').absolute()}")