/**
 * MatrixText — vanilla JS port of the React MatrixText component
 * Each letter flashes as a random 0/1 in accent color, then resolves to the real char.
 */

class MatrixText {
  constructor(el, options = {}) {
    this.el = el;
    this.text = el.dataset.text || el.textContent.trim();
    this.initialDelay   = options.initialDelay   ?? parseInt(el.dataset.initialDelay   || '200');
    this.letterDuration = options.letterDuration  ?? parseInt(el.dataset.letterDuration || '500');
    this.letterInterval = options.letterInterval  ?? parseInt(el.dataset.letterInterval || '80');

    this._build();
    setTimeout(() => this._animate(), this.initialDelay);
  }

  _build() {
    this.el.textContent = '';
    this.spans = this.text.split('').map((char) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.display = 'inline-block';
      span.style.fontVariantNumeric = 'tabular-nums';
      span.style.transition = 'color 0.1s ease, text-shadow 0.1s ease';
      span._finalChar = char;
      span._isSpace = char === ' ';
      this.el.appendChild(span);
      return span;
    });
  }

  _animate() {
    let i = 0;
    const next = () => {
      if (i >= this.spans.length) return;
      this._animateLetter(this.spans[i]);
      i++;
      setTimeout(next, this.letterInterval);
    };
    next();
  }

  _animateLetter(span) {
    if (span._isSpace) return;

    const randomChar = Math.random() > 0.5 ? '1' : '0';
    span.textContent = randomChar;
    span.style.color = '#21c9d0';
    span.style.textShadow = '0 0 12px rgba(33,201,208,0.7), 0 0 30px rgba(33,201,208,0.3)';

    setTimeout(() => {
      span.textContent = span._finalChar;
      span.style.color = '';
      span.style.textShadow = '';
    }, this.letterDuration);
  }

  static init(selector = '[data-matrix-text]') {
    document.querySelectorAll(selector).forEach(el => new MatrixText(el));
  }
}

document.addEventListener('DOMContentLoaded', () => MatrixText.init());
