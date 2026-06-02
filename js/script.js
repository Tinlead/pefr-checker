function calculateFERF() {
    const age = parseFloat(document.getElementById('age').value);
    const height = parseFloat(document.getElementById('height').value);
    const gender = document.getElementById('gender').value;
    const measuredPefr = parseFloat(document.getElementById('fev').value);

    if (!age || !height || !gender || !measuredPefr) {
        alert('กรุณากรอกข้อมูลให้ครบถ้วน');
        return;
    }

    if (age < 0 || age > 120) {
        alert('กรุณากรอกอายุที่ถูกต้อง');
        return;
    }

    if (height < 50 || height > 250) {
        alert('กรุณากรอกส่วนสูงที่ถูกต้อง');
        return;
    }

    let standardPefr = getPdfStandardPefr(age, height, gender);
    let source = 'pdf';
    if (standardPefr === null) {
        // fallback: use formula-predicted PEFR and note the source
        standardPefr = calculatePredictedPEFR(age, height, gender);
        source = 'formula';
    }
    displayResults(age, height, gender, measuredPefr, standardPefr, source);
}

function calculatePredictedPEFR(age, height, gender) {
    const heightMeters = height / 100;
    let pefr;

    if (age < 15) {
        // เด็กอายุต่ำกว่า 15 ปี ใช้สูตรเฉพาะ
        pefr = ((height - 100) * 5) + 100;
    } else if (gender === 'male') {
        pefr = (((heightMeters * 5.48) + 1.58) - (age * 0.041)) * 60;
    } else {
        pefr = (((heightMeters * 3.72) + 2.24) - (age * 0.03)) * 60;
    }

    if (pefr < 100) {
        pefr = 100;
    }

    return Math.round(pefr);
}

function getPdfStandardPefr(age, height, gender) {
    if (!window.PEFR_TABLE) {
        return null;
    }

    const table = PEFR_TABLE[gender];
    if (!table) {
        return null;
    }

    const nearestHeight = Math.round(height / 2) * 2;
    const heightIndex = table.heights.indexOf(nearestHeight);
    if (heightIndex === -1) {
        return null;
    }

    const ageKey = String(Math.round(age));
    const row = table.values[ageKey];
    if (!row) {
        return null;
    }

    return row[heightIndex] || null;
}

function displayResults(age, height, gender, measured, predicted, source) {
    document.getElementById('result-age').textContent = age + ' ปี';
    document.getElementById('result-height').textContent = height + ' ซม.';
    document.getElementById('result-gender').textContent = gender === 'male' ? 'ชาย' : 'หญิง';
    document.getElementById('result-fev').textContent = measured + ' L/min';
    
    const percentage = (measured / predicted) * 100;
    const percentageText = percentage.toFixed(2) + ' %';
    document.getElementById('result-ferf').textContent = percentageText;

    let firstLine = '';
    let messageText = '';
    let statusText = '';

    if (source === 'pdf') {
        const relation = measured >= predicted ? 'มากกว่ามาตรฐาน' : 'น้อยกว่ามาตรฐาน';
        firstLine = 'ผลลัพธ์ : ' + percentage.toFixed(2) + '% ของมาตรฐาน (' + relation + ')';
        messageText = firstLine;
    } else {
        const relation = measured >= predicted ? 'มากกว่ามาตรฐาน' : 'น้อยกว่ามาตรฐาน';
        const diff = measured - predicted;
        const diffAbs = Math.abs(diff);
        const diffPercent = (diff / predicted) * 100;
        firstLine = 'ผลลัพธ์ : ' + percentage.toFixed(2) + '% ของมาตรฐาน (' + relation + ')';
        messageText = firstLine;
    }

    if (percentage >= 80) {
        statusText = 'ค่าปกติ - สมรรถภาพปอดอยู่ในเกณฑ์ปกติ';
    } else if (percentage >= 60) {
        statusText = 'ผิดปกติเพียงเล็กน้อย - PEFR ต่ำกว่าปกติเล็กน้อย';
    } else if (percentage >= 40) {
        statusText = 'ผิดปกติปานกลาง - PEFR ลดลงอย่างเห็นได้ชัด';
    } else if (percentage >= 25) {
        statusText = 'ผิดปกติรุนแรง - PEFR ลดลงมาก';
    } else {
        statusText = 'ผิดปกติรุนแรงมาก - PEFR ลดลงมากเกินไป';
    }

    document.getElementById('result-message').innerHTML = messageText;
    document.getElementById('result-status').textContent = statusText;
    document.getElementById('form-ferf').style.display = 'none';
    document.getElementById('result-container').style.display = 'block';
    document.querySelector('.container').scrollIntoView({ behavior: 'smooth', block: 'start' });

    saveResultToGoogleSheets();
}

function resetForm() {
    // Reset form
    document.getElementById('form-ferf').reset();
    
    // Hide results and show form
    document.getElementById('form-ferf').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';
}

// Allow Enter key to submit form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-ferf');
    if (form) {
        form.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                calculateFERF();
            }
        });
    }
});