import Phaser from "phaser";
import { getFileFromS3 } from "../../utils/s3";

export default class CustomLoader extends Phaser.Loader.LoaderPlugin {
    s3Image(key: string, s3Key: string) {
        this.addFile(new S3ImageFile(this, key, s3Key));
    }
}

class S3ImageFile extends Phaser.Loader.File {
    constructor(
        loader: Phaser.Loader.LoaderPlugin,
        key: string,
        s3Key: string
    ) {
        super(loader, {
            type: "image",
            key: key,
            url: s3Key,
            xhrSettings: undefined,
        });
    }

    async load() {
        try {
            const url = await getFileFromS3(this.url as string);
            this.src = url;
            this.loader.nextFile(this, true);
        } catch (error) {
            console.error(`Failed to load asset ${this.key} from S3:`, error);
            this.loader.nextFile(this, false);
        }
    }
}

