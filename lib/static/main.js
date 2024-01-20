const colorPicker = new iro.ColorPicker('#picker', {
    width: 400,
    height: 400,
    borderWidth: 2,
    borderColor: '#ffffff',
    color: '#ff0000'
});

function hexToRgb(hex) {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    }
}

function changeColor() {
    fetch('/set-rgb-color', {
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify(colorPicker.color.rgb),
        method: 'PUT'
    }).then((response) => {
        if (!response.ok) {
            console.error(response.text());
        }
    })
}

function breath() {

    fetch('/breath', {
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify({
            r: colorPicker.color.rgb['r'],
            g: colorPicker.color.rgb['g'],
            b: colorPicker.color.rgb['b'],
            delay: document.getElementById('cycle-delay').value
        }),
        method: 'PUT'
    }).then((response) => {
        if (!response.ok) {
            console.error(response.text());
        }
    })
}

function cycle() {
    const first = hexToRgb(document.getElementById('first-color').value);
    const second = hexToRgb(document.getElementById('second-color').value);

    fetch('/cycle', {
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify({
            c1r: first.r,
            c1g: first.g,
            c1b: first.b,
            c2r: second.r,
            c2g: second.g,
            c2b: second.b,
            delay: document.getElementById('cycle-delay').value
        }),
        method: 'PUT'
    }).then((response) => {
        if (!response.ok) {
            console.error(response.text())
        }
    })
}

function candyTornado() {
    fetch('/candy-tornado', {
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify({
            sat: document.getElementById('sat').value,
            val: document.getElementById('val').value ,
            delay_ms: document.getElementById('delay').value,
            hue_gap: document.getElementById('gap').value,
            hue_cycle_speed: document.getElementById('cycle-speed').value,
         }),
        method: 'PUT'
    }).then((response) => {
        if (!response.ok) {
            console.error(response.text());
        }
    })
}
