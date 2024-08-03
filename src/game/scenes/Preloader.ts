import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor ()
    {
        super('Preloader');
    }

    init ()
    {
        //  We loaded this image in our Boot Scene, so we can display it here
        this.add.image(512, 384, 'background');

        //  A simple progress bar. This is the outline of the bar.
        this.add.rectangle(512, 384, 468, 32).setStrokeStyle(1, 0xffffff);

        //  This is the progress bar itself. It will increase in size from the left based on the % of progress.
        const bar = this.add.rectangle(512-230, 384, 4, 28, 0xffffff);

        //  Use the 'progress' event emitted by the LoaderPlugin to update the loading bar
        this.load.on('progress', (progress: number) => {

            //  Update the progress bar (our bar is 464px wide, so 100% = 464px)
            bar.width = 4 + (460 * progress);

        });
    }

    preload ()
    {
        //  Load the assets for the game - Replace with your own assets
        this.load.setPath('assets');
        //Chessboard tile
        this.load.image('tile1', 'images/tile.png');
        this.load.image('tile2', 'images/tile2.png');

        //Chess pieces
        this.load.image('pawn_w', 'images/pawn_w.png');
        this.load.image('pawn_b', 'images/pawn_b.png');
        this.load.image('bishop_b', 'images/bishop_b.png');
        this.load.image('bishop_w', 'images/bishop_w.png');
        this.load.image('king_b', 'images/king_b.png');
        this.load.image('king_w', 'images/king_w.png');
        this.load.image('queen_w', 'images/queen_w.png');
        this.load.image('queen_b', 'images/queen_b.png');
        this.load.image('knight_w', 'images/knight_w.png');
        this.load.image('knight_b', 'images/knight_b.png');
        this.load.image('rook_w', 'images/rook_w.png');
        this.load.image('rook_b', 'images/rook_b.png');

        this.load.tilemapTiledJSON('isochess', 'tilemap/isochess.json' );
     
    }

    create ()
    {
        //  When all the assets have loaded, it's often worth creating global objects here that the rest of the game can use.
        //  For example, you can define global animations here, so we can use them in other scenes.

        //  Move to the MainMenu. You could also swap this for a Scene Transition, such as a camera fade.
        this.scene.start('MainMenu');
    }
}