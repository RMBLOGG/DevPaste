import uuid
import secrets
from datetime import datetime, timezone, timedelta


def generate_slug(length: int = 8) -> str:
    """Generate a short unique slug from UUID."""
    return uuid.uuid4().hex[:length]


def generate_delete_token() -> str:
    """Generate a secure random delete token."""
    return secrets.token_urlsafe(24)


def calculate_expiry(expiration: str) -> str | None:
    """Calculate expiry datetime from option string. Returns ISO string or None."""
    now = datetime.now(timezone.utc)
    mapping = {
        'never': None,
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
    """Check if a paste has expired."""
    if expires_at is None:
        return False
    now = datetime.now(timezone.utc)
    try:
        expiry = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        return now > expiry
    except (ValueError, AttributeError):
        return False


def format_datetime(dt_str: str | None) -> str:
    """Format datetime string for display."""
    if not dt_str:
        return 'Unknown'
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%b %d, %Y at %H:%M UTC')
    except (ValueError, AttributeError):
        return dt_str


def time_ago(dt_str: str | None) -> str:
    """Return human-readable time ago string."""
    if not dt_str:
        return 'Unknown'
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = now - dt

        seconds = int(diff.total_seconds())
        if seconds < 60:
            return 'just now'
        elif seconds < 3600:
            m = seconds // 60
            return f'{m} minute{"s" if m != 1 else ""} ago'
        elif seconds < 86400:
            h = seconds // 3600
            return f'{h} hour{"s" if h != 1 else ""} ago'
        elif seconds < 2592000:
            d = seconds // 86400
            return f'{d} day{"s" if d != 1 else ""} ago'
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
