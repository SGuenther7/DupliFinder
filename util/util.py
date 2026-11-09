
import os
import hashlib
import json

from pathlib import Path
from math import log10


def formatBytes(byte_count: int) -> str:
    suffix = ["B", "KB", "MB", "GB"]
    try:
        index = min(int(log10(byte_count) // 3), 3)
    except:
        index = 0
    
    tmp = f"{byte_count / (1000 ** index)}".split(".")
    
    if index == 0:
        return f"{tmp[0]} {suffix[index]}"
    else:
        return f"{tmp[0]}.{tmp[1][:3]} {suffix[index]}"
    
def printDict(dictionary:dict) -> None:
    for key in dictionary:
        print(dictionary[key])
    print(f"length: {len(dictionary)}")
    
def loadCache(file: str) -> dict:

    hashes = dict()

    try:
        with open(file, "r") as f:
            hashes = json.load(f)
    except:
        print(f"loading cach file \"{file}\" FAILED")
        hashes = dict()

    return hashes

# deletes hashes from deleted/moved files
def validateCache(dictionary: dict) -> dict:

    new_hashes = dict()

    for hash in dictionary:

        new_values = [val for val in dictionary[hash] if Path(val).exists()]

        if len(new_values) > 0:
            new_hashes[hash] = new_values
        # else:
            # all files were deleted/moved
            # -> do not add

    return new_hashes

def getDupes(hashes: dict):
    # single = dict()
    # multiple = dict()
    # for hash in new_hashes:
    #     files = new_hashes[hash]
    #     if len(files) == 1:
    #         single[hash] = files
    #     else:
    #         multiple[hash] = files

    # new_hashes.clear()
    # new_hashes.update(multiple)
    # new_hashes.update(single)

    # print(len(multiple))

    dupes = dict()

    for hash in hashes:
        files = hashes[hash]
        if len(files) > 1:
            dupes[hash] = files

    return dupes

def addNewHashes(target_dirs: list[str], hashes:dict) -> dict:
    file_paths = []

    for path in target_dirs:
        for (root, dirs, files) in os.walk(path):
            file_paths += [root + "/" + f for f in files]

    already_hashed = [j for sub in hashes.values() for j in sub]
    to_hash = [i for i in file_paths if i not in already_hashed]
    
    print("---------------")
    print(f"Loaded {len(already_hashed)} cached hashes")

    items = 0
    amount = len(to_hash)
    hashed_bytes = 0

    # calculate hashes and check duplicates
    for file in to_hash:
        with open(file.replace("\\", "/"), "rb") as f:
            hash = hashlib.file_digest(f, "sha256").hexdigest()
            items += 1
            print(f"  {items} / {amount} ({int((items/amount) * 100)}%) {util.formatBytes(os.path.getsize(file))}"
                  + "       ", end="\r\r")

            tmp = hashes.get(hash, [])
            tmp += [file]            
            hashes[hash] = tmp

        # save between every 10 GB processed
        hashed_bytes += os.path.getsize(file)
        if hashed_bytes > 10_000_000_000:
            hashed_bytes = 0
            saveCache(hashes, results_file)

    return hashes

def saveCache(cache:dict, file: str) -> None:

    with open(file, "w") as tmp:
        json.dump(cache, tmp)
        
def displayDupes(dupes: dict, filter: list[str], display_min_size: int) -> None:

    file_filtered = open("filtered.txt", "w", encoding="utf8")

    print("---------------")
    print("---------------", file=file_filtered)
    
    dupes_found = 0
    
    for hash in dupes:
        files = dupes[hash]

        if os.path.getsize(files[0]) < display_min_size:
            continue

        if len(files) > 1:

            if True in [files[0].endswith(i) for i in filter]:
                continue

            found = len(files[1:])
            dupes_found += found

            print(f"found {found} ({formatBytes(os.path.getsize(files[0]))}) dupes:")
            print(f"found {found} ({formatBytes(os.path.getsize(files[0]))}) dupes:", file=file_filtered)
            print(f"\tOLD: {files[0]}")
            print(f"\tOLD: {files[0]}", file=file_filtered)

            for file in files[1:]:
                print(f"\tNEW: {file}")
                print(f"\tNEW: {file}", file=file_filtered)

    print("---------------")
    print("---------------", file=file_filtered)
    print(f"FOUND: {dupes_found} dupes")
    print(f"FOUND: {dupes_found} dupes", file=file_filtered)
    print("---------------")
    print("---------------", file=file_filtered)
    print("---------------")
    print("---------------", file=file_filtered)

    file_filtered.close()


def orderDupes(dupes: dict) -> dict:
    mult = dict()
    single = dict()

    for hash in dupes:
        files = dupes[hash]
        if len(files) > 1:
            mult[hash] = files
        else:
            single[hash] = files

    mult.update(single)

    return mult