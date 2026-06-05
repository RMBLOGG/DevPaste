from flask import Blueprint, render_template, request, redirect, url_for, abort, Response, flash
from app.models import create_paste, get_paste_by_slug, increment_views, delete_paste, get_public_pastes, get_paste_stats
from app.utils import is_expired, time_ago, format_datetime, SUPPORTED_LANGUAGES

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '').strip()
        language = request.form.get('language', 'plaintext')
        visibility = request.form.get('visibility', 'public')
        expiration = request.form.get('expiration', 'never')

        if not content:
            flash('Content cannot be empty.', 'error')
            return render_template('index.html', languages=SUPPORTED_LANGUAGES,
                                   form_data=request.form)

        paste = create_paste(title, content, language, visibility, expiration)
        if not paste:
            flash('Failed to create paste. Please try again.', 'error')
            return render_template('index.html', languages=SUPPORTED_LANGUAGES,
                                   form_data=request.form)

        return redirect(url_for('main.view_paste', slug=paste['slug'],
                                _external=False) + f'?token={paste["delete_token"]}')

    return render_template('index.html', languages=SUPPORTED_LANGUAGES, form_data={})


@main.route('/paste/<slug>')
def view_paste(slug: str):
    paste = get_paste_by_slug(slug)
    if not paste:
        abort(404)

    if is_expired(paste.get('expires_at')):
        return render_template('404.html', message='This paste has expired.'), 404

    # Increment views (fire-and-forget style)
    increment_views(slug)

    delete_token = request.args.get('token', '')

    return render_template('view.html',
                           paste=paste,
                           delete_token=delete_token,
                           time_ago=time_ago,
                           format_datetime=format_datetime,
                           languages=SUPPORTED_LANGUAGES)


@main.route('/raw/<slug>')
def raw_paste(slug: str):
    paste = get_paste_by_slug(slug)
    if not paste:
        abort(404)
    if is_expired(paste.get('expires_at')):
        return Response('This paste has expired.', status=404, mimetype='text/plain')
    return Response(paste['content'], mimetype='text/plain; charset=utf-8')


@main.route('/delete/<slug>', methods=['POST'])
def delete_paste_route(slug: str):
    token = request.form.get('delete_token', '')
    success = delete_paste(slug, token)
    if success:
        flash('Paste deleted successfully.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid delete token or paste not found.', 'error')
        return redirect(url_for('main.view_paste', slug=slug))


@main.route('/explore')
def explore():
    search = request.args.get('q', '').strip()
    language = request.args.get('lang', '').strip()
    page = max(1, int(request.args.get('page', 1)))
    per_page = 18
    offset = (page - 1) * per_page

    pastes = get_public_pastes(limit=per_page + 1, offset=offset, search=search, language=language)
    has_next = len(pastes) > per_page
    pastes = pastes[:per_page]

    stats = get_paste_stats()

    return render_template('explore.html',
                           pastes=pastes,
                           search=search,
                           language=language,
                           languages=SUPPORTED_LANGUAGES,
                           page=page,
                           has_next=has_next,
                           time_ago=time_ago,
                           stats=stats)
