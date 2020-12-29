DATA_URL = "https://en.wikiquote.org/w/api.php?format=json&action=parse&prop=text&page=Main_Page"

def is_text(chunk, prev=None):
        if chunk == b'n' and prev == b'\\':
            return False
        if chunk in (b'\\',):
            return False
        return True

def get_qotd(requests):
    resp = requests.get(DATA_URL)
    print("Wikiquote: Got response. parsing...")

    in_xml = False
    in_quote = False
    quote_buf = b''
    read_buf = [b'']*16
    prev = b''

    for chunk in resp.iter_content(chunk_size=1):
        if chunk == b'<':
            in_xml = True
        if in_xml and chunk == b'>':
            in_xml = False
        elif not in_xml:
            if prev == b';' and b''.join(read_buf) == b'of the day&#160;':
                in_quote = True
            elif in_quote and quote_buf[-2:] == b' ~':
                in_quote = False
                break
            if is_text(chunk, prev):
                if in_quote:
                    quote_buf += chunk
                else:
                    del read_buf[0]
                    read_buf.append(chunk)
        prev = chunk

    return quote_buf.decode('utf-8')