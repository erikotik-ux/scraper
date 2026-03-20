/**
 * SpecialText — vanilla JS port of tom_ui/special-text
 * Two-phase scramble animation: random fill → left-to-right reveal
 */

const RANDOM_CHARS = "_!X$0-+*#";

function getRandomChar(prevChar) {
  let char;
  do {
    char = RANDOM_CHARS[Math.floor(Math.random() * RANDOM_CHARS.length)];
  } while (char === prevChar);
  return char;
}

class SpecialText {
  constructor(el, options = {}) {
    this.el = el;
    this.text = el.dataset.text || el.textContent.trim();
    this.speed = options.speed ?? parseInt(el.dataset.speed) || 20;
    this.delay = options.delay ?? parseFloat(el.dataset.delay) || 0;
    this.inView = options.inView ?? el.dataset.inview === "true" || false;
    this.once = options.once ?? el.dataset.once !== "false";

    this.phase = "phase1";
    this.animationStep = 0;
    this.intervalId = null;
    this.startTimeoutId = null;
    this.hasStarted = false;
    this.hasAnimated = false;

    this.el.textContent = "\u00A0".repeat(this.text.length);

    if (this.inView) {
      this._observeInView();
    } else {
      this._scheduleStart();
    }
  }

  _scheduleStart() {
    if (this.delay > 0) {
      this.startTimeoutId = setTimeout(() => this._startAnimation(), this.delay * 1000);
    } else {
      this._startAnimation();
    }
  }

  _observeInView() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (this.once) observer.disconnect();
            if (!this.hasAnimated || !this.once) this._scheduleStart();
          } else if (!this.once && this.hasAnimated) {
            this._reset();
          }
        });
      },
      { rootMargin: "-100px" }
    );
    observer.observe(this.el);
  }

  _startAnimation() {
    this.hasStarted = true;
    this.hasAnimated = true;
    this.phase = "phase1";
    this.animationStep = 0;
    this.el.textContent = "\u00A0".repeat(this.text.length);
    this._tick();
  }

  _reset() {
    clearInterval(this.intervalId);
    clearTimeout(this.startTimeoutId);
    this.hasStarted = false;
    this.intervalId = null;
    this._scheduleStart();
  }

  _tick() {
    if (this.intervalId) clearInterval(this.intervalId);
    this.intervalId = setInterval(() => {
      if (this.phase === "phase1") this._runPhase1();
      else this._runPhase2();
    }, this.speed);
  }

  _runPhase1() {
    const maxSteps = this.text.length * 2;
    const currentLength = Math.min(this.animationStep + 1, this.text.length);
    const chars = [];

    for (let i = 0; i < currentLength; i++) {
      chars.push(getRandomChar(i > 0 ? chars[i - 1] : undefined));
    }
    for (let i = currentLength; i < this.text.length; i++) {
      chars.push("\u00A0");
    }

    this.el.textContent = chars.join("");

    if (this.animationStep < maxSteps - 1) {
      this.animationStep++;
    } else {
      this.phase = "phase2";
      this.animationStep = 0;
    }
  }

  _runPhase2() {
    const revealedCount = Math.floor(this.animationStep / 2);
    const chars = [];

    for (let i = 0; i < revealedCount && i < this.text.length; i++) {
      chars.push(this.text[i]);
    }
    if (revealedCount < this.text.length) {
      chars.push(this.animationStep % 2 === 0 ? "_" : getRandomChar());
    }
    for (let i = chars.length; i < this.text.length; i++) {
      chars.push(getRandomChar());
    }

    this.el.textContent = chars.join("");

    if (this.animationStep < this.text.length * 2 - 1) {
      this.animationStep++;
    } else {
      this.el.textContent = this.text;
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  destroy() {
    clearInterval(this.intervalId);
    clearTimeout(this.startTimeoutId);
  }

  static init(selector = "[data-special-text]") {
    document.querySelectorAll(selector).forEach((el) => new SpecialText(el));
  }
}

window.SpecialText = SpecialText;
