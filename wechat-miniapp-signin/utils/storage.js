const RECORD_KEY = 'attendance_records';

function getRecords() {
  return wx.getStorageSync(RECORD_KEY) || [];
}

function addRecord(record) {
  const records = getRecords();
  records.unshift(record);
  wx.setStorageSync(RECORD_KEY, records);
  return records;
}

function clearRecords() {
  wx.removeStorageSync(RECORD_KEY);
}

module.exports = {
  getRecords,
  addRecord,
  clearRecords
};
