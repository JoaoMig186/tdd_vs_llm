const Reservation = require("../src/reservation");

describe("Reservation", () => {

  test("cria reserva válida", () => {
    const r = new Reservation("A1", new Date("2025-01-01T10:00"), new Date("2025-01-01T11:00"));

    expect(r.roomId).toBe("A1");
    expect(r.startTime.getHours()).toBe(10);
    expect(r.endTime.getHours()).toBe(11);
  });

  test("não permite reserva com horário invertido", () => {
    expect(() => {
      new Reservation("A1", new Date("2025-01-01T11:00"), new Date("2025-01-01T10:00"));
    }).toThrow();
  });

  test("não permite horário de início igual ao fim", () => {
    expect(() => {
      new Reservation("A1", new Date("2025-01-01T10:00"), new Date("2025-01-01T10:00"));
    }).toThrow();
  });

});
