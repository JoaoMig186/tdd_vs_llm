class Reservation {
  constructor(roomId, startTime, endTime) {
    if (startTime >= endTime) {
      throw new Error("Horário de início deve ser anterior ao horário de fim");
    }
    
    this.roomId = roomId;
    this.startTime = startTime;
    this.endTime = endTime;
  }
}

module.exports = Reservation;
