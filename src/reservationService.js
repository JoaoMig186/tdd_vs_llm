const Reservation = require('./reservation');

class ReservationService {
  constructor() {
    this.rooms = [];
    this.reservations = [];
  }

  addRoom(room) {
    this.rooms.push(room);
  }

  getRooms() {
    return this.rooms;
  }

  createReservation(roomId, startTime, endTime) {
    // Verificar se a sala existe
    const roomExists = this.rooms.some(room => room.id === roomId);
    if (!roomExists) {
      throw new Error("Sala não encontrada");
    }

    // Verificar conflitos de horário
    const hasConflict = this.reservations.some(reservation => {
      if (reservation.roomId !== roomId) {
        return false;
      }

      // Verificar sobreposição de horários
      return (
        (startTime >= reservation.startTime && startTime < reservation.endTime) ||
        (endTime > reservation.startTime && endTime <= reservation.endTime) ||
        (startTime <= reservation.startTime && endTime >= reservation.endTime)
      );
    });

    if (hasConflict) {
      throw new Error("Conflito de horário: sala já reservada para este período");
    }

    // Criar a reserva
    const reservation = new Reservation(roomId, startTime, endTime);
    this.reservations.push(reservation);

    return reservation;
  }

  getReservations(roomId) {
    return this.reservations.filter(r => r.roomId === roomId);
  }
}

module.exports = ReservationService;
