import { Scene } from "phaser";

export class Preloader extends Scene {
    constructor() {
        super("Preloader");
    }

    init() {
        this.add.image(512, 384, "background");

        this.add.rectangle(512, 384, 468, 32).setStrokeStyle(1, 0xffffff);

        const bar = this.add.rectangle(512 - 230, 384, 4, 28, 0xffffff);

        this.load.on("progress", (progress: number) => {
            bar.width = 4 + 460 * progress;
        });
    }

    preload() {
        this.load.setPath("assets");

        //Chessboard tiles
        this.load.image("tile1", "images/tile.png");
        this.load.image("tile2", "images/tile2.png");

        //Chess pieces
        this.load.image("pawn_w", "images/pawn_w.png");
        this.load.image("pawn_b", "images/pawn_b.png");
        this.load.image("bishop_b", "images/bishop_b.png");
        this.load.image("bishop_w", "images/bishop_w.png");
        this.load.image("king_b", "images/king_b.png");
        this.load.image("king_w", "images/king_w.png");
        this.load.image("queen_w", "images/queen_w.png");
        this.load.image("queen_b", "images/queen_b.png");
        this.load.image("knight_w", "images/knight_w.png");
        this.load.image("knight_b", "images/knight_b.png");
        this.load.image("rook_w", "images/rook_w.png");
        this.load.image("rook_b", "images/rook_b.png");

        this.load.spritesheet("heroine", "sprites/Light with FX.png");
        this.load.spritesheet("dark_heroine", "sprites/Dark with FX.png");

        this.load.tilemapTiledJSON("isochess", "tilemap/isochess.json");
    }

    create() {
        this.scene.start("MainMenu");
    }
}

