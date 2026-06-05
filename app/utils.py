import uuid
import secrets
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))


def generate_slug(length: int = 8) -> str:
    return uuid.uuid4().hex[:length]


def generate_delete_token() -> str:
    return secrets.token_urlsafe(24)


def calculate_expiry(expiration: str) -> str | None:
    now = datetime.now(timezone.utc)
    mapping = {
        'never': None,
        '1j': timedelta(hours=1),
        '1h': timedelta(hours=1),
        '1d': timedelta(days=1),
        '7d': timedelta(days=7),
        '30d': timedelta(days=30),
    }
    delta = mapping.get(expiration)
    if delta is None:
        return None
    return (now + delta).isoformat()


def is_expired(expires_at: str | None) -> bool:
    if expires_at is None:
        return False
    now = datetime.now(timezone.utc)
    try:
        expiry = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        return now > expiry
    except (ValueError, AttributeError):
        return False


def format_datetime(dt_str: str | None) -> str:
    if not dt_str:
        return 'Tidak diketahui'
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        dt_wib = dt.astimezone(WIB)
        return dt_wib.strftime('%d %b %Y, %H:%M WIB')
    except (ValueError, AttributeError):
        return dt_str


def time_ago(dt_str: str | None) -> str:
    if not dt_str:
        return 'Tidak diketahui'
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - dt

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return 'baru saja'
        elif seconds < 3600:
            m = seconds // 60
            return f'{m} menit lalu'
        elif seconds < 86400:
            h = seconds // 3600
            return f'{h} jam lalu'
        elif seconds < 2592000:
            d = seconds // 86400
            return f'{d} hari lalu'
        else:
            return format_datetime(dt_str)
    except (ValueError, AttributeError):
        return dt_str


SUPPORTED_LANGUAGES = [
    ('plaintext', 'Plain Text'),
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('typescript', 'TypeScript'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('java', 'Java'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('csharp', 'C#'),
    ('go', 'Go'),
    ('rust', 'Rust'),
    ('php', 'PHP'),
    ('ruby', 'Ruby'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('sql', 'SQL'),
    ('bash', 'Bash/Shell'),
    ('json', 'JSON'),
    ('yaml', 'YAML'),
    ('xml', 'XML'),
    ('markdown', 'Markdown'),
    ('dockerfile', 'Dockerfile'),
    ('nginx', 'Nginx'),
]
