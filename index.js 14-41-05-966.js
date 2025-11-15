class Reservation {
  constructor(room, date, startTime, endTime, requester) {
    this.room = room;
    this.date = date;
    this.startTime = startTime;
    this.endTime = endTime;
    this.requester = requester;
    this.id = Date.now() + Math.random();
    this.status = 'active';
  }
}

class Room {
  constructor(name, capacity) {
    this.name = name;
    this.capacity = capacity;
  }
}

class ReservationService {
  constructor() {
    this.reservations = [];
  }

  createReservation(room, date, startTime, endTime, requester) {
    // Validar campos obrigatórios
    if (!room || !date || !startTime || !endTime || !requester) {
      throw new Error('Todos os campos são obrigatórios');
    }

    // Validar coerência de horários
    if (startTime >= endTime) {
      throw new Error('Hora de início deve ser anterior à hora de fim');
    }

    // Validar data no passado
    const reservationDate = new Date(date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (reservationDate < today) {
      throw new Error('Não é possível fazer reservas para datas passadas');
    }

    // Verificar conflitos de horário
    const hasConflict = this.reservations.some(reservation => {
      if (reservation.status !== 'active') {
        return false;
      }

      if (reservation.room !== room || reservation.date !== date) {
        return false;
      }

      // Verificar sobreposição de horários
      const existingStart = reservation.startTime;
      const existingEnd = reservation.endTime;

      return (
        (startTime >= existingStart && startTime < existingEnd) ||
        (endTime > existingStart && endTime <= existingEnd) ||
        (startTime <= existingStart && endTime >= existingEnd)
      );
    });

    if (hasConflict) {
      throw new Error('Conflito de horário: sala já reservada para este período');
    }

    // Criar a reserva
    const reservation = new Reservation(room, date, startTime, endTime, requester);
    this.reservations.push(reservation);

    return reservation;
  }

  listReservations() {
    return this.reservations.filter(r => r.status === 'active');
  }

  cancelReservation(reservationId) {
    const reservation = this.reservations.find(r => r.id === reservationId);

    if (!reservation) {
      throw new Error('Reserva não encontrada');
    }

    if (reservation.status === 'cancelled') {
      throw new Error('Reserva já foi cancelada');
    }

    reservation.status = 'cancelled';
    return reservation;
  }

  getAllReservations() {
    return this.reservations;
  }
}

module.exports = {
  Reservation,
  Room,
  ReservationService
};
