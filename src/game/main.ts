import { Boot } from "./scenes/Boot";
import { GameOver } from "./scenes/GameOver";
import { Chessboard as PauseMenu } from "./scenes/ChessBoard";
import { Intro } from "./scenes/Intro";
import { Platformer as MainGame } from "./scenes/Platformer";
import { FinalBattle } from "./scenes/FinalBattle";
import { MainMenu } from "./scenes/MainMenu";
import { AUTO, Game } from "phaser";
import { Preloader } from "./scenes/Preloader";

//  Find out more information about the Game Config at:
//  https://newdocs.phaser.io/docs/3.70.0/Phaser.Types.Core.GameConfig
const config: Phaser.Types.Core.GameConfig = {
    type: AUTO,
    width: 1024,
    height: 768,
    parent: "game-container",
    backgroundColor: "transparent",
    scene: [
        Boot,
        Preloader,
        MainMenu,
        Intro,
        PauseMenu,
        MainGame,
        FinalBattle,
        GameOver,
    ],
};

const StartGame = (parent: string) => {
    return new Game({ ...config, parent });
};

export default StartGame;

