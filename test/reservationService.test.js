const ReservationService = require("../src/reservationService");
const Room = require("../src/room");

describe("ReservationService", () => {

  let service;

  beforeEach(() => {
    service = new ReservationService();

    service.addRoom(new Room("A1", "Sala Azul"));
    service.addRoom(new Room("B1", "Sala Vermelha"));
  });

  test("adicionar sala", () => {
    expect(service.getRooms().length).toBe(2);
  });

  test("criar reserva válida", () => {
    service.createReservation("A1",
      new Date("2025-01-01T09:00"),
      new Date("2025-01-01T10:00")
    );

    const res = service.getReservations("A1");
    expect(res.length).toBe(1);
  });

  test("não permite reserva com sala inexistente", () => {
    expect(() =>
      service.createReservation("X",
        new Date("2025-01-01T09:00"),
        new Date("2025-01-01T10:00")
      )
    ).toThrow();
  });

  test("não permite reservas sobrepostas", () => {
    service.createReservation("A1",
      new Date("2025-01-01T09:00"),
      new Date("2025-01-01T10:00")
    );

    // sobrepõe totalmente
    expect(() =>
      service.createReservation("A1",
        new Date("2025-01-01T09:30"),
        new Date("2025-01-01T10:30")
      )
    ).toThrow();

    // começa antes e termina dentro
    expect(() =>
      service.createReservation("A1",
        new Date("2025-01-01T08:30"),
        new Date("2025-01-01T09:30")
      )
    ).toThrow();

    // começa dentro e termina depois
    expect(() =>
      service.createReservation("A1",
        new Date("2025-01-01T09:30"),
        new Date("2025-01-01T10:30")
      )
    ).toThrow();
  });

  test("permite reserva em outra sala mesmo horário", () => {
    service.createReservation("A1",
      new Date("2025-01-01T09:00"),
      new Date("2025-01-01T10:00")
    );

    expect(() =>
      service.createReservation("B1",
        new Date("2025-01-01T09:00"),
        new Date("2025-01-01T10:00")
      )
    ).not.toThrow();
  });

});
