from app import supabase
from app.utils import generate_slug, generate_delete_token, calculate_expiry, is_expired
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def create_paste(title: str, content: str, language: str, visibility: str, expiration: str) -> dict | None:
    """Insert a new paste into Supabase and return the created record."""
    slug = generate_slug()
    # Ensure slug uniqueness
    for _ in range(5):
        existing = get_paste_by_slug(slug)
        if not existing:
            break
        slug = generate_slug()

    delete_token = generate_delete_token()
    expires_at = calculate_expiry(expiration)

    data = {
        'slug': slug,
        'title': title.strip() if title and title.strip() else None,
        'content': content,
        'language': language,
        'visibility': visibility,
        'delete_token': delete_token,
        'views': 0,
        'expires_at': expires_at,
    }

    try:
        resp = supabase.table('pastes').insert(data).execute()
        if resp.data:
            return resp.data[0]
        return None
    except Exception as e:
        logger.error(f'Error creating paste: {e}')
        return None


def get_paste_by_slug(slug: str) -> dict | None:
    """Fetch a paste by slug."""
    try:
        resp = supabase.table('pastes').select('*').eq('slug', slug).limit(1).execute()
        if resp.data:
            return resp.data[0]
        return None
    except Exception as e:
        logger.error(f'Error fetching paste {slug}: {e}')
        return None


def increment_views(slug: str) -> None:
    """Increment the view count for a paste."""
    try:
        paste = get_paste_by_slug(slug)
        if paste:
            supabase.table('pastes').update({'views': paste['views'] + 1}).eq('slug', slug).execute()
    except Exception as e:
        logger.error(f'Error incrementing views for {slug}: {e}')


def delete_paste(slug: str, delete_token: str) -> bool:
    """Delete a paste if the token matches. Returns True on success."""
    try:
        paste = get_paste_by_slug(slug)
        if not paste:
            return False
        if paste.get('delete_token') != delete_token:
            return False
        supabase.table('pastes').delete().eq('slug', slug).execute()
        return True
    except Exception as e:
        logger.error(f'Error deleting paste {slug}: {e}')
        return False


def get_public_pastes(limit: int = 30, offset: int = 0, search: str = '', language: str = '') -> list[dict]:
    """Fetch public pastes with optional search and language filter."""
    try:
        query = supabase.table('pastes').select(
            'id, slug, title, language, visibility, views, created_at, expires_at'
        ).eq('visibility', 'public').order('created_at', desc=True).range(offset, offset + limit - 1)

        resp = query.execute()
        pastes = resp.data or []

        # Filter out expired pastes
        active = [p for p in pastes if not is_expired(p.get('expires_at'))]

        # Filter by language
        if language:
            active = [p for p in active if p.get('language') == language]

        # Filter by search (title)
        if search:
            s = search.lower()
            active = [p for p in active if
                      (p.get('title') and s in p['title'].lower()) or s in p.get('language', '').lower()]

        return active
    except Exception as e:
        logger.error(f'Error fetching public pastes: {e}')
        return []


def get_paste_stats() -> dict:
    """Get basic platform stats."""
    try:
        resp = supabase.table('pastes').select('id', count='exact').execute()
        total = resp.count or 0
        pub_resp = supabase.table('pastes').select('id', count='exact').eq('visibility', 'public').execute()
        public = pub_resp.count or 0
        return {'total': total, 'public': public}
    except Exception as e:
        logger.error(f'Error fetching stats: {e}')
        return {'total': 0, 'public': 0}
