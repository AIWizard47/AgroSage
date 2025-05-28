import re

def format_ai_response_to_html(text):
    # Replace bold markers with <strong> tags
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Replace numbered lists (1., 2., etc.) with bullet-style spacing
    text = re.sub(r'(\n\d+\.)', r'<br>\1', text)

    # Convert line breaks to HTML <br> or paragraphs
    paragraphs = text.strip().split('\n')
    html_paragraphs = [f'<p>{line.strip()}</p>' for line in paragraphs if line.strip()]

    return '\n'.join(html_paragraphs)
