SEP: bytes = b"\r\n"
COL: bytes = b":"
SPC: bytes = b" "

HTTP1_0: bytes = b"HTTP/1.0"
HTTP1_1: bytes = b"HTTP/1.1"

STATUS = {
	100: b"100 Continue",
	101: b"101 Switching Protocols",
	200: b"200 OK",
	204: b"204 No Content",
	206: b"206 Partial Content",
	301: b"301 Moved Permanently",
	308: b"308 Permanent Redirect",
	400: b"400 Bad Request",
	401: b"401 Unauthorized",
	403: b"403 Forbidden",
	404: b"404 Not Found",
	405: b"405 Method Not Allowed",
	408: b"408 Request Timeout",
	410: b"410 Gone",
	413: b"413 Content Too Large",
	414: b"414 URI Too Long",
	415: b"415 Unsupported Media Type",
	426: b"426 Upgrade Required",
	429: b"429 Too Many Requests",
	431: b"431 Request Header Fields Too Large",
	451: b"451 Unavailable For Legal Reasons",
	500: b"500 Internal Server Error",
	501: b"501 Not Implemented",
	502: b"502 Bad Gateway",
	503: b"503 Service Unavailable",
	504: b"504 Gateway Timeout",
	505: b"505 HTTP Version Not Supported",
	508: b"508 Loop Detected",
	511: b"511 Network Authentication Required"
}

CONTENT_DISPOSITION: bytes = b"Content-Disposition"
CONTENT_LANGUAGE: bytes = b"Content-Language"
CONTENT_LENGTH: bytes = b"Content-Length"
CONTENT_LOCATION: bytes = b"Content-Location"
CONTENT_MD5: bytes = b"Content-MD5"
CONTENT_RANGE: bytes = b"Content-Range"
CONTENT_TRANSFER_ENCODING: bytes = b"Content-Transfer-Encoding"

CACHE_ALL: bytes = b"Cache-Control: max-age=31536000, immutable"
CACHE_NONE: bytes = b"Cache-Control: no-cache"

CONTENT_TYPE: bytes = b"Content-Type"
MIME_TYPES = {
	"html": b"text/html",
	"text": b"text/plain",
	"json": b"application/json",
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
MIME_IMG = {'ico', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'svg', 'tif', 'tiff', 'webp'}
MIME_TXT = {'html', 'text', 'js', 'css'}
