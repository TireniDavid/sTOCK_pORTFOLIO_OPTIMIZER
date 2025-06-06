// static/js/indicators.js

function computeSMA(data, period) {
    let smaArray = [];
    for (let i = period - 1; i < data.length; i++) {
        let sum = 0;
        for (let j = i - period + 1; j <= i; j++) {
            sum += data[j].Close;
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
    for (let i = 0; i < period; i++) {
        sum += data[i].Close;
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
