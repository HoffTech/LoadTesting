import re

AMMO_TMPL = u'''\
{method} {url} HTTP/1.1\r
Host: {host}\r
User-Agent: yandex-tank/1.1.1\r
{headers}\r
\r
{body}\r
'''

NL = '\r\n'


def gen_request(method, url, host, headers, body=None):
    assert isinstance(headers, dict)
    assert not body or isinstance(body, str)
    if body:
        headers['Content-Length'] = len(str(body).encode("utf-8"))
    body = body if body else ''

    ammo = AMMO_TMPL.format(
        method=method.upper(), host=host, url=url,
        headers=NL.join("%s: %s" % (n, v) for (n, v) in headers.items()),
        body=(body.replace("'", '"') + NL) if body else '')
    print('%s\n%s' % (len(str(ammo).encode("utf-8")), ammo))
    return '%s\n%s' % (len(str(ammo).encode("utf-8")), ammo)


def make_ammo(method, url, headers, body):
    req_template = (
        "%s %s HTTP/1.1\r"
        "%s\r"
        "\r\n"
    )

    req_template_w_entity_body = (
        "%s %s HTTP/1.1\r"
        "%s\r"
        "Content-Length: %d\r"
        "\r"
        "%s\r\n"
    )

    if not body:
        req = req_template % (method, url, headers)
    else:
        rusLen = len(re.findall('[а-яё]', body, re.I))
        req = req_template_w_entity_body % (method, url, headers, len(body) - rusLen + rusLen*2, body)

    ammo_template = (
        "%d \n"
        "%s"
    )
    rusL = len(re.findall('[а-яё]', req, re.I))
    return ammo_template % (len(req) - rusL + rusL*2 + 6, req)

