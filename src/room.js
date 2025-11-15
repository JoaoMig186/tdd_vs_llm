class Room {
  constructor(id, name) {
    if (!name || name.trim() === "") {
      throw new Error("Nome da sala não pode ser vazio");
    }
    
    this.id = id;
    this.name = name;
  }
}

module.exports = Room;
