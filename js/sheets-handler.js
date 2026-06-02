// 1. นำ URL ที่ได้จากการ Deploy Web App ของ Google Apps Script มาใส่ที่นี่
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzRklV27YGtya5V8a0M2wca2PY6PGQeHM8_hS7b9BMYbi5ZY8SG7WwDnwQJliDk2S9fZQ/exec';

async function saveResultToGoogleSheets() {
    // 1. ดึงข้อความดิบจากหน้าเว็บออกมาก่อน
    const ageRaw = document.getElementById('result-age').textContent;       // เช่น "25 ปี"
    const heightRaw = document.getElementById('result-height').textContent; // เช่น "170 ซม."
    const genderRaw = document.getElementById('result-gender').textContent; // เช่น "ชาย" หรือ "หญิง"
    const pefrRaw = document.getElementById('result-fev').textContent;     // เช่น "450 L/min"
    const percentageRaw = document.getElementById('result-ferf').textContent; // เช่น "ค่าปกติ - ..."

    // 2. ตกแต่งข้อมูลเล็กน้อย (ตัดเอาหน่วยอย่าง "ปี", "ซม.", "L/min" ออกเพื่อให้เหลือตัวเลขสวยๆ บน Sheet)
    const payload = {
        age: parseFloat(ageRaw) || ageRaw,
        height: parseFloat(heightRaw) || heightRaw,
        gender: genderRaw,
        measuredPefr: parseFloat(pefrRaw) || pefrRaw,
        result: percentageRaw // ส่งไปเป็น data.result ตามที่ Apps Script รอรับ
    };

    try {
        // 3. ยิงข้อมูลไปที่ Apps Script
        await fetch(GOOGLE_SCRIPT_URL, {
            method: 'POST',
            mode: 'no-cors', // แนะนำให้ใช้คู่กับ Google Apps Script Web App
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log('บันทึกข้อมูลเรียบร้อย!');
    } catch (error) {
        console.error('ไม่สามารถบันทึกข้อมูลได้:', error);
    }
}