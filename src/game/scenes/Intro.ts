import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class Intro extends Scene {
    constructor() {
        super('Intro');
      }

    preload() {
        // Load assets
    }

    create() {
        // Create environment and characters
         
        EventBus.emit('current-scene-ready', this);
    }

    update() {
        // Update logic
    }

    changeScene() {
        this.scene.start('MainGame');
      }

}