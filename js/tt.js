const SHEET_ID = "1u7F7oTauwCKCrLaL0aCeNkK1F_PtgFocIvQD66mYj2w";
const SHEET_NAME = "PEFR";

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    
    const newRow = [
      data.age,
      data.height,
      data.gender,
      data.measuredPefr,
      data.result,
      new Date()
    ];
    
    sheet.appendRow(newRow);
    
    return ContentService
      .createTextOutput(JSON.stringify({ 
        success: true, 
        message: "บันทึกข้อมูลสำเร็จ" 
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ 
        success: false, 
        message: "เกิดข้อผิดพลาด: " + error.toString() 
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}