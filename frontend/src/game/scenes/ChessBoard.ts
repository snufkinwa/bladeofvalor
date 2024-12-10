import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class Chessboard extends Scene {
  camera: Phaser.Cameras.Scene2D.Camera;
  map: Phaser.Tilemaps.Tilemap;
  boardLayer: Phaser.Tilemaps.TilemapLayer | null;
  piecesLayer: Phaser.Tilemaps.TilemapLayer | null;
  selectedPiece: Phaser.Tilemaps.Tile | null;

  constructor() {
    super('PauseMenu');
    this.selectedPiece = null;
  }

  preload() {
    // Load the tilemap JSON
    this.load.tilemapTiledJSON('isochess', 'tilemap/isochess.json');

    // Load each individual image referenced in the tilesets array
    this.load.image('tile2', 'assets/images/tile2.png');
    this.load.on('filecomplete-image-tile2', () => console.log('tile2 image loaded'));
  
    this.load.image('tile', 'assets/images/tile.png');
    this.load.image('pawn_b', 'assets/images/pawn_b.png');
    this.load.image('rook_b', 'assets/images/rook_b.png');
    this.load.image('knight_b', 'assets/images/knight_b.png');
    this.load.image('bishop_b', 'assets/images/bishop_b.png');
    this.load.image('queen_b', 'assets/images/queen_b.png');
    this.load.image('bishop_w', 'assets/images/bishop_w.png');
    this.load.image('knight_w', 'assets/images/knight_w.png');
    this.load.image('queen_w', 'assets/images/queen_w.png');
    this.load.image('king_w', 'assets/images/king_w.png');
    this.load.image('king_b', 'assets/images/king_b.png');
    this.load.image('rook_w', 'assets/images/rook_w.png');
    this.load.image('pawn_w', 'assets/images/pawn_w.png');
  }

  create() {
    this.camera = this.cameras.main;
    this.camera.setZoom(2);
    this.camera.centerOn(0, 0);

    // Create the tilemap
    this.map = this.add.tilemap('isochess');
    console.log(this.map);

    // Add the tilesets
    const tileset2 = this.map.addTilesetImage('tile2.png', 'tile2');
    console.log('tileset2:', tileset2);
    const tileset = this.map.addTilesetImage('tile.png', 'tile');
    const pawn_b = this.map.addTilesetImage('pawn_b.png', 'pawn_b');
    const rook_b = this.map.addTilesetImage('rook_b.png', 'rook_b');
    const knight_b = this.map.addTilesetImage('knight_b.png', 'knight_b');
    const bishop_b = this.map.addTilesetImage('bishop_b.png', 'bishop_b');
    const queen_b = this.map.addTilesetImage('queen_b.png', 'queen_b');
    const bishop_w = this.map.addTilesetImage('bishop_w.png', 'bishop_w');
    const knight_w = this.map.addTilesetImage('knight_w.png', 'knight_w');
    const queen_w = this.map.addTilesetImage('queen_w.png', 'queen_w');
    const king_w = this.map.addTilesetImage('king_w.png', 'king_w');
    const king_b = this.map.addTilesetImage('king_b.png', 'king_b');
    const rook_w = this.map.addTilesetImage('rook_w.png', 'rook_w');
    const pawn_w = this.map.addTilesetImage('pawn_w.png', 'pawn_w');

    

    const validTilesets1 = [tileset2, tileset].filter((t): t is Phaser.Tilemaps.Tileset => t !== null);
    this.boardLayer = this.map.createLayer('Tile Layer 1', validTilesets1, 0, 0);
    
    const validTilesets2 = [pawn_b, rook_b, knight_b, bishop_b, queen_b, bishop_w, knight_w, queen_w, king_w, king_b, rook_w, pawn_w].filter((t): t is Phaser.Tilemaps.Tileset => t !== null);
    this.piecesLayer = this.map.createLayer('Tile Layer 2', validTilesets2, 8, -20);


    this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
      //@ts-ignore
      const tile = this.map.getTileAtWorldXY(pointer.worldX, pointer.worldY, true, this.camera, this.piecesLayer);
      if (tile && tile.index !== -1) {
        this.selectedPiece = tile;
        console.log('Selected Piece:', tile);
      } else {
        if (this.selectedPiece) {
          //@ts-ignore
          const targetTile = this.map.getTileAtWorldXY(pointer.worldX, pointer.worldY, true, this.camera, this.boardLayer);
          if (targetTile) {
            this.movePiece(this.selectedPiece, targetTile.x, targetTile.y);
            this.selectedPiece = null;
          }
        }
      }
    });

    EventBus.emit('current-scene-ready', this);
  }

  movePiece(piece: Phaser.Tilemaps.Tile, tileX: number, tileY: number) {
    if (this.piecesLayer) {
      // Remove piece from current position
      this.piecesLayer.removeTileAt(piece.x, piece.y);

      // Place piece at new position
      this.piecesLayer.putTileAt(piece.index, tileX, tileY);

      // Log the new position of the piece
      console.log(`Moved piece to (${tileX}, ${tileY})`);

      // Refresh the layer to ensure the piece is displayed correctly
      this.piecesLayer.setCollisionByExclusion([-1]); // Optional, set collision if needed
    }
  }

  changeScene() {
    this.scene.start('GameOver');
  }
}