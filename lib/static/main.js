const el = id => document.getElementById(id);

let popupTimeout;

function showPopup(message) {
    const popup = document.getElementById('feedback-popup');
    popup.textContent = message;

    popup.classList.remove('show', 'fade-out');
    clearTimeout(popupTimeout);

    void popup.offsetWidth;

    popup.classList.add('show');

    popupTimeout = setTimeout(() => {
        popup.classList.remove('show');
        popup.classList.add('fade-out');
    }, 1200);
}

document.getElementById('feedback-popup').addEventListener('transitionend', (e) => {
    if (e.propertyName === 'opacity') {
        e.target.classList.remove('fade-out');
    }
});

function sendJSON(url, data) {
    return fetch(url, {
        method: 'PUT',
        headers: { "Content-Type": "application/json; charset=UTF-8" },
        body: JSON.stringify(data)
    }).then(res => {
        if (res.ok) {
             showPopup("Color successfully changed!");
        } else {
             showPopup(`${res.status}: ${res.statusText}`); 
        }
    });
}

function hexToRgb(hex) {
    const m = hex.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
    return m ? {
        r: parseInt(m[1], 16),
        g: parseInt(m[2], 16),
        b: parseInt(m[3], 16)
    } : null;
}

const pickerSize = Math.min(window.innerWidth - 40, 400);

const colorPicker = new iro.ColorPicker('#picker', {
    width: pickerSize,
    height: pickerSize,
    borderWidth: 2,
    borderColor: '#ffffff',
    color: '#ff0000'
});

document.querySelectorAll('.buttons').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.classList.remove('pressed');
        void btn.offsetWidth;
        btn.classList.add('pressed');
    });
});

function off() {
    sendJSON('/set-rgb-color', { r: 0, g: 0, b: 0 });
}

function changeColor() {
    sendJSON('/set-rgb-color', colorPicker.color.rgb);
}

function breath() {
    sendJSON('/breath', {
        ...colorPicker.color.rgb,
        delay: el('cycle-delay').value
    });
}

function cycle() {
    const c1 = hexToRgb(el('first-color').value);
    const c2 = hexToRgb(el('second-color').value);

    sendJSON('/cycle', {
        c1r: c1.r, c1g: c1.g, c1b: c1.b,
        c2r: c2.r, c2g: c2.g, c2b: c2.b,
        delay: el('cycle-delay').value
    });
}

function candyTornado() {
    sendJSON('/candy-tornado', {
        sat: el('sat').value,
        val: el('val').value,
        delay_ms: el('delay').value,
        hue_gap: el('gap').value,
        hue_cycle_speed: el('cycle-speed').value
    });
}
