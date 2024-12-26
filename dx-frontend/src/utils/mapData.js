import {reactive} from "vue";
import EnemyIconPath from "@/assets/map/enemy.png";
import ChestIconPath from "@/assets/map/chest.png";
import GateIconPath from "@/assets/map/gate.png";
import ShopIconPath from "@/assets/map/shop.png";
import NPCIconPath from "@/assets/map/npc.png";
import TrapIconPath from "@/assets/map/trap.png";
import PuzzleIconPath from "@/assets/map/puzzle.png";
import DeathIconPath from "@/assets/map/death.png";
import QuestIconPath from "@/assets/map/quest.png";

const EnemyIcon = new Image();
EnemyIcon.src = EnemyIconPath;
const ChestIcon = new Image();
ChestIcon.src = ChestIconPath;
const GateIcon = new Image();
GateIcon.src = GateIconPath;
const ShopIcon = new Image();
ShopIcon.src = ShopIconPath;
const NPCIcon = new Image();
NPCIcon.src = NPCIconPath;
const TrapIcon = new Image();
TrapIcon.src = TrapIconPath;
const PuzzleIcon = new Image();
PuzzleIcon.src = PuzzleIconPath;
const DeathIcon = new Image();
DeathIcon.src = DeathIconPath;
const QuestIcon = new Image();
QuestIcon.src = QuestIconPath;


const RoomLabel = {
    ENEMY: {value: "enemy", label: "Enemy",},
    CHEST: {value: "chest", label: "Chest",},
    GATE: {value: "gate", label: "Gate",},
    SHOP: {value: "shop", label: "Shop",},
    NPC: {value: "npc", label: "NPC",},
    TRAP: {value: "trap", label: "Trap",},
    PUZZLE: {value: "puzzle", label: "Puzzle",},
    DEATH: {value: "death", label: "Death",},
    QUEST: {value: "quest", label: "Quest",},

    getIcon(value) {
        switch (value) {
            case "enemy":
                return EnemyIcon;
            case "chest":
                return ChestIcon;
            case "gate":
                return GateIcon;
            case "shop":
                return ShopIcon;
            case "npc":
                return NPCIcon;
            case "trap":
                return TrapIcon;
            case "puzzle":
                return PuzzleIcon;
            case "death":
                return DeathIcon;
            case "quest":
                return QuestIcon;
            default:
                return undefined;
        }
    }
};



const MapData = reactive({
    rooms: [],
    connections: [],
    verticalConnections: [], // To handle vertical connections like stairs or lifts

    addRoom(room) {
        this.rooms.push(room); // Reactive updates trigger re-renders
        this.save();
    },

    updateRoom(room) {
        const index = this.rooms.findIndex((r) => r.id === room.id);
        if (index !== -1) {
            this.rooms[index] = room;
            this.save();
        }
    },

    addConnection(connection) {
        this.connections.push(connection);
        this.save();
    },

    addVerticalConnection(connection) {
        // check if connection already exists
        const exists = this.verticalConnections.some(
            (c) =>
                c.room_a === connection.room_b || c.room_b === connection.room_a
        );
        if (exists) {
            console.log("Connection already exists", {connection}, this.verticalConnections);
            return;
        }
        this.verticalConnections.push(connection);
        this.save();
    },

    save() {
        localStorage.setItem(
            "mapData",
            JSON.stringify({
                rooms: this.rooms,
                connections: this.connections,
                virtualConnections: this.verticalConnections,
            })
        );
    },

    load() {
        const storedData = localStorage.getItem("mapData");
        if (storedData) {
            const parsed = JSON.parse(storedData);
            this.rooms = parsed.rooms || [];
            this.connections = parsed.connections || [];
            this.verticalConnections = parsed.virtualConnections || [];
            this.characters = parsed.characters || {};
        }
    },

    toJSON() {
        return JSON.stringify({
            rooms: this.rooms,
            connections: this.connections,
            virtualConnections: this.verticalConnections,
            characters: {},
        });
    },

    fromJSON(json) {
        this.rooms = json.rooms || [];
        this.connections = json.connections || [];
        this.verticalConnections = json.virtualConnections || [];
        this.characters = json.characters || {};
    },

    clear() {
        this.rooms = [];
        this.connections = [];
        this.verticalConnections = [];
        this.characters = {};
        this.save();
    },

    getRoomById(id) {
        return this.rooms.find((room) => room.id === id);
    },

    getRoomByCoords(x, y, z) {
        return this.rooms.find(
            (room) => room.grid_x === x && room.grid_y === y && room.grid_z === z
        );
    },

    createRoomIfNotExists(name, x, y, z) {
        let room = this.getRoomByCoords(x, y, z);
        if (!room) {
            room = createRoomDTO({name: name, grid_x: x, grid_y: y, grid_z: z});
            this.addRoom(room);
        }
        return room;
    },

    getValidConnections(floor) {
        return this.connections.filter(
            (connection) => {
                const roomA = this.getRoomById(connection.room_a);
                const roomB = this.getRoomById(connection.room_b);
                return roomA !== undefined && roomB !== undefined && roomA.grid_z === floor && roomB.grid_z === floor
            }
        );
    },
    getValidVerticalConnections(floor) {
        return this.verticalConnections.filter(
            (connection) => {
                const roomA = this.getRoomById(connection.room_a);
                const roomB = this.getRoomById(connection.room_b);
                return roomA !== undefined && roomB !== undefined && ((roomA.grid_z === floor) || (roomB.grid_z === floor))
            }
        );
    },
    getCharactersInRoom(room) {
        return this.characters[room.id] || [];
    }
});

const RoomType = {
    DEFAULT: {value: "default", label: "Default", color: "lightblue"},
    START: {value: "start", label: "Start", color: "green"},
    HUB: {value: "hub", label: "Hub", color: "purple"},
    BOSS: {value: "boss", label: "Boss", color: "red"},
    END: {value: "end", label: "End", color: "darkblue"},
};

function createRoomDTO({id, name, type, grid_x, grid_y, grid_z}) {
    return {
        id: id || Date.now(),
        name: name || "New Room",
        type: type || RoomType.DEFAULT.value,
        grid_x: grid_x || 0,
        grid_y: grid_y || 0,
        grid_z: grid_z || 0,
        label: "",
    };
}

export {RoomType, MapData, createRoomDTO, RoomLabel};
export default MapData;
