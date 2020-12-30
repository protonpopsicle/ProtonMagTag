DATA_URL = "https://en.wikiquote.org/w/api.php?format=json&action=parse&prop=text&page=Main_Page"

def get_qotd(requests):
    resp = requests.get(DATA_URL)
    print("Wikiquote: Got response. parsing...")

    prev = b''
    in_xml = False
    in_escape_seq = False
    in_quote = False
    quote_buf = b''
    read_buf = [b'']*16
    it = resp.iter_content(chunk_size=1)

    for char in it:
        if char == b'<':
            in_xml = True
        if in_xml and char == b'>':
            in_xml = False
        elif not in_xml:
            # skip some stuff
            if char in b'\\':
                prev = char
                continue
            if prev == b'\\':
                if char == b'n':
                    prev = char
                    continue
                if char == b'u':
                    for x in range(4):
                       prev = next(it)
                    continue

            if not in_quote and b''.join(read_buf) == b'of the day&#160;':
                in_quote = True
            elif in_quote and quote_buf[-2:] == b' ~':
                in_quote = False
                break
            if in_quote:
                quote_buf += char
            else:
                del read_buf[0]
                read_buf.append(char)
        prev = char

    return quote_buf.decode('utf-8')
