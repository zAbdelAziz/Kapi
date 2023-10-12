SEP: bytes = b"\r\n"
COL: bytes = b":"
SPC: bytes = b" "

HTTP1_0: bytes = b"HTTP/1.0"
HTTP1_1: bytes = b"HTTP/1.1"

STATUS_100: bytes = b"100 Continue"
STATUS_101: bytes = b"101 Switching Protocols"
STATUS_200: bytes = b"200 OK"
STATUS_204: bytes = b"204 No Content"
STATUS_206: bytes = b"206 Partial Content"
STATUS_301: bytes = b"301 Moved Permanently"
STATUS_308: bytes = b"308 Permanent Redirect"
STATUS_400: bytes = b"400 Bad Request"
STATUS_401: bytes = b"401 Unauthorized"
STATUS_403: bytes = b"403 Forbidden"
STATUS_404: bytes = b"404 Not Found"
STATUS_405: bytes = b"405 Method Not Allowed"
STATUS_408: bytes = b"408 Request Timeout"
STATUS_410: bytes = b"410 Gone"
STATUS_413: bytes = b"413 Content Too Large"
STATUS_414: bytes = b"414 URI Too Long"
STATUS_415: bytes = b"415 Unsupported Media Type"
STATUS_426: bytes = b"426 Upgrade Required"
STATUS_429: bytes = b"429 Too Many Requests"
STATUS_431: bytes = b"431 Request Header Fields Too Large"
STATUS_451: bytes = b"451 Unavailable For Legal Reasons"
STATUS_500: bytes = b"500 Internal Server Error"
STATUS_501: bytes = b"501 Not Implemented"
STATUS_502: bytes = b"502 Bad Gateway"
STATUS_503: bytes = b"503 Service Unavailable"
STATUS_504: bytes = b"504 Gateway Timeout"
STATUS_505: bytes = b"505 HTTP Version Not Supported"
STATUS_508: bytes = b"508 Loop Detected"
STATUS_511: bytes = b"511 Network Authentication Required"

CONTENT_TYPE: bytes = b"Content-Type"
CONTENT_DISPOSITION: bytes = b"Content-Disposition"
CONTENT_ENCODING: bytes = b"Content-Encoding"
CONTENT_LANGUAGE: bytes = b"Content-Language"
CONTENT_LENGTH: bytes = b"Content-Length"
CONTENT_LOCATION: bytes = b"Content-Location"
CONTENT_MD5: bytes = b"Content-MD5"
CONTENT_RANGE: bytes = b"Content-Range"
CONTENT_TRANSFER_ENCODING: bytes = b"Content-Transfer-Encoding"

HTML_TYPE: bytes = b"text/html"
JSON_TYPE: bytes = b"application/json"

CACHE_ALL: bytes = b"Cache-Control: max-age=31536000, immutable"
CACHE_NONE: bytes = b"Cache-Control: no-cache"


MIME_TYPES = {
	"js": b"text/javascript",
	"css": b"text/css",
	"ico": b"image/vnd.microsoft.icon",
	"bmp": b"image/bmp",
	"gif": b"image/gif",
	"jpg": b"image/jpeg",
	"jpeg": b"image/jpeg",
	"png": b"image/png",
	"svg": b"image/svg+xml",
	"tif": b"image/tif",
	"tiff": b"image/tif",
	"webp": b"image/webp",
}
