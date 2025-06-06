// my_app/static/js/indicator.js

function computeSMA(data, period) {
    let smaArray = [];
    for (let i = period - 1; i < data.length; i++) {
        let sum = 0;
        if (new Date(data[i].Date * 1000).toISOString().slice(0,10) === "1990-06-12") {
            console.log("Raw Close values for index", i, ":", data.slice(i - period + 1, i + 1).map(item => item.Close));
        }
        for (let j = i - period + 1; j <= i; j++) {
            sum += Number(data[j].Close);
        }
        smaArray.push({
            time: new Date(data[i].Date * 1000).toISOString().slice(0,10),
            value: sum / period
        });
    }
    return smaArray;
}

function computeEMA(data, period) {
    let emaArray = [];
    let multiplier = 2 / (period + 1);
    let sum = 0;
    // Log the raw Close values for a specific date if needed.
    if (new Date(data[i].Date * 1000).toISOString().slice(0,10) === "1990-06-12") {
        console.log("Raw Close values for index", i, ":", data.slice(i - period + 1, i + 1).map(item => item.Close));
    }
    for (let i = 0; i < period; i++) {
        sum += Number(data[i].Close);
    }
    let emaPrev = sum / period;
    emaArray.push({
        time: new Date(data[period - 1].Date * 1000).toISOString().slice(0,10),
        value: emaPrev
    });
    for (let i = period; i < data.length; i++) {
        emaPrev = (data[i].Close - emaPrev) * multiplier + emaPrev;
        emaArray.push({
            time: new Date(data[i].Date * 1000).toISOString().slice(0,10),
            value: emaPrev
        });
    }
    return emaArray;
}

// Expose globally
window.computeSMA = computeSMA;
window.computeEMA = computeEMA;
