const Room = require("../src/room");

describe("Room", () => {

  test("criar sala com id e nome", () => {
    const room = new Room("A1", "Sala de Reunião");
    expect(room.id).toBe("A1");
    expect(room.name).toBe("Sala de Reunião");
  });

  test("nome da sala não pode ser vazio", () => {
    expect(() => new Room("A2", "")).toThrow();
  });

});
