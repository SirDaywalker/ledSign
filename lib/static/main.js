const el = id => document.getElementById(id);

const settingIDs = {
    breathSpeed: 'breath-speed',
    cycleDelay: 'cycle-delay',
    cycleFirstColor: 'cycle-first-color',
    cycleSecondColor: 'cycle-second-color',
    lotteryDelay: 'lottery-delay',
    lotteryMainColor: 'lottery-main-color',
    lotteryBallsColor: 'lottery-balls-color',
    tornadoSaturation: 'tornado-saturation',
    tornadoValue: 'tornado-value',
    tornadoDelay: 'tornado-delay',
    tornadoGap: 'tornado-gap',
    tornadoSpeed: 'tornado-speed'
};

let settings = JSON.parse(localStorage.getItem('settings'));
loadSettings();

function loadSettings() {
    if (!settings) {
        updateSettings();
        settings = JSON.parse(localStorage.getItem('settings'));
        return;
    }

    for (const [key, id] of Object.entries(settingIDs)) {
        el(id).value = settings[key];
    }
}

function updateSettings() {
    const newSettings = {};

    for (const [key, id] of Object.entries(settingIDs)) {
        newSettings[key] = el(id).value;
    }

    settings = newSettings;
    localStorage.setItem('settings', JSON.stringify(settings));
}

const popover = document.getElementById("settings-container");
popover.addEventListener("toggle", (e) => {
    if (!popover.matches(":popover-open")) {
        updateSettings()
    }
})

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
    } : -1;
}

const pickerSize = Math.min(window.innerWidth - 40, 400);

const colorPicker = new iro.ColorPicker('#color-picker', {
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
        delay: settings.cycleDelay
    });
}

function cycle() {
    const c1 = hexToRgb(settings.cycleFirstColor);
    const c2 = hexToRgb(settings.cycleSecondColor);

    sendJSON('/cycle', {
        c1r: c1.r, c1g: c1.g, c1b: c1.b,
        c2r: c2.r, c2g: c2.g, c2b: c2.b,
        delay: settings.cycleDelay
    });
}

function lottery() {
    const main = hexToRgb(settings.lotteryMainColor);
    const balls = hexToRgb(settings.lotteryBallsColor);

    sendJSON('/lottery', {
        mr: main.r, mg: main.g, mb: main.b,
        br: balls.r, bg: balls.g, bb: balls.b,
        delay: settings.lotteryDelay
    })
}

function candyTornado() {
    sendJSON('/candy-tornado', {
        sat: settings.tornadoSaturation,
        val: settings.tornadoValue,
        delay_ms: settings.tornadoDelay,
        hue_gap: settings.tornadoGap,
        hue_cycle_speed: settings.tornadoSpeed
    });
}
