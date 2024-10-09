def count_symbols(text):
    letters = dict()

    for item in text:
        if item not in letters.keys():
            letters[item] = 1
        else:
            letters[item] += 1

    return letters

def c_indx(text):
    l = len(text)
    if l < 2:return 0
    s = 0
    
    for f in count_symbols(text).values():
        s += f * (f -1)

    return s / (l * (l -1))

if __name__ == "__main__":
    import os
    import sys

    try:
        f_list = os.listdir(sys.argv[1])
    except (FileNotFoundError, NotADirectoryError, IndexError):
        print("No such directory.")
        exit()

    offset = len(max(f_list, key=len))+10
    print(f"{'Files' :<{offset}} Values")
    print("-" * (offset +20))
    for file in f_list:
        if ".txt" in file:
            p_file = f"{sys.argv[1]}/{file}"
            t = open(p_file, "r").read()
            print(f"{p_file :<{offset}} {c_indx(t)}")
