from decimal import Decimal, getcontext
import random

getcontext().prec = 50

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
freqMono = {'о': 0.13407122044703443, 'е': 0.08105676907131823, 'н': 0.07174844046385201, 'а': 0.07163110859064865, 'т': 0.055400199464184445, 'и': 0.05418777010774977, 'с': 0.049572716428417776, 'л': 0.047988736140172475, 'в': 0.04356923558284608, 'р': 0.0414963724895868, 'п': 0.03283336918473904, 'д': 0.03205115669671666, 'к': 0.03156227389170268, 'м': 0.029078749242231652, 'у': 0.027338326456381876, 'ы': 0.025656569607133778, 'б': 0.021549954045016327, 'я': 0.02043530124958445, 'з': 0.020181082190977178, 'г': 0.01988775250796879, 'ь': 0.018890431585740268, 'ч': 0.013571386667188141, 'ж': 0.011361636388524943, 'й': 0.011068306705516553, 'ю': 0.00901499892445783, 'х': 0.008858556426853355, 'ш': 0.005827483035766666, 'щ': 0.0040479496255157715, 'э': 0.003774175254707941, 'ц': 0.0012710952930363533, 'ъ': 0.0005084381172145413, 'ф': 0.0005084381172145413}

# a = {}
# for i in freqMono:
#     a[i] = float(freqMono[i])
# print(a)


def encrypt(m, k) -> str:
    i = (ALPHABET.find(m) + ALPHABET.find(k)) % len(ALPHABET)
    return ALPHABET[i]


def encrypt_stream(pt: str, stream_key) -> str:
    ct = ""
    for m in pt:
        ct += encrypt(m, stream_key.next())

    return ct


def decrypt(c, k) -> str:
    i = (ALPHABET.find(c) - ALPHABET.find(k)) % len(ALPHABET)
    return ALPHABET[i]


def decrypt_stream(ct: str, stream_key) -> str:
    pt = ""
    for c in ct:
        pt += decrypt(c, stream_key.next())
        
    return pt


# Index of coincidence
def ic(text: str) -> float:
    alph = {i: 0 for i in ALPHABET}
    for i in text:
        if i not in ALPHABET:
            raise Exception("Invalid letter")

        alph[i] += 1

    summ = 0
    for v in alph.values():
        summ += v * (v - 1)

    return summ / (sum(alph.values()) * (sum(alph.values())-1)) 


def colision_stat(text: str, r: int) -> int:
    stat = 0
    for i in range(len(text)-r):
        if text[i] == text[i+r]:
            stat += 1
    return stat


def prepare_text(text: str) -> str:
    out = ""
    for i in text:
        if i.lower() not in ALPHABET:
            continue

        out += i.lower()

    return out


def frequencies(text: str) -> dict[str, float]:
    freq = {i: 0 for i in ALPHABET}
    for i in text:
        if i not in ALPHABET:
            raise Exception("Invalid letter")

        freq[i] += 1

    count = sum(freq.values())
    for k in freq:
        freq[k] /= count

    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))


class VigenereKeyStream:
    key: str
    key_len: int
    offset: int = 0

    def __init__(self, key: str):
        for i in key:
            if i not in ALPHABET:
                raise Exception("Invalid key")
        
        self.key = key
        self.key_len = len(key)

    def reset(self):
        self.offset = 0

    def next(self) -> str:
        s = self.key[self.offset]
        self.offset = (self.offset + 1) % self.key_len
        return s


def main():

    keys = ["а", "вы", "дуб", "ночь", "огонь", "вопрос", "медведь", "мельница", "организмы", "предложить", "преподавать", "исследовать", "неопределенность", "профессионально", "непредсказуемость", "систематизированный"]
    # long_keys = ["".join(random.choices(ALPHABET, k=i)) for i in range(10, 41)]
    # keys += long_keys

    print("Keys:", keys)

    text = ""
    with open("/home/user/uni/crypro-24-25/lab2/perebynos_fb-22_vlasenko_fb-22_cp2/texts/pt.txt", "r") as f:
        text = f.read()
    pt = prepare_text(text)
    
    print("IC0:", 1/len(ALPHABET))

    print("IC(pt):", ic(pt))
    for i in keys:
        ks = VigenereKeyStream(i)
        ct = encrypt_stream(pt, ks)
        print(f"IC(pt ct r={len(i)}):", ic(ct))
    
    text = ""
    with open("/home/user/uni/crypro-24-25/lab2/perebynos_fb-22_vlasenko_fb-22_cp2/texts/2_ct.txt", "r") as f:
        text = f.read()
    ct = prepare_text(text)


    print("IC(ct):", ic(ct))    
    for i in range(14, 15):
        print(f"IC(ct r={i})", ic(ct[::i]))


    # key_len = 14
    # for k in range(1):

    #     key = ""
    #     for i in range(key_len):

    #         freq = frequencies(ct[i::key_len])
    #         print(f"Letter {i}:", freq)
    #         c = list(freq.keys())[0]
    #         key += decrypt(c, list(freqMono.keys())[k])

    #     print(key)

    # keyfrag = ["фэ", "ьу", "яц", "рлщ", "ук", "йт", "ты", "цин", "ч", "тд", "ьу", "х", "ьу", "ю"]
    # def reqout(part, symbols):
    #     if len(part) >= 14:
    #         print(part)
    #         return
    #     mb = symbols[:1][0]
    #     for i in mb:
    #         i = decrypt(i, list(freqMono.keys())[0])
    #         reqout(part+i, symbols[1:])

    # reqout("", keyfrag)

    ks = VigenereKeyStream("последнийдозор")
    print(decrypt_stream(ct, ks))
    # print(decrypt("з", "ь"))
    # print("PT:", text[:50])
    # key_stream = VigenereKeyStream("козак")
    # ct = encrypt_stream(text, key_stream)
    # print("CT:", ct[:50])
    # key_stream.reset()
    # pt2 = decrypt_stream(ct, key_stream)
    # print("PT2:", pt2[:50])


if __name__=="__main__":
    main()
