import {
    S3Client,
    GetObjectCommand,
    GetObjectCommandOutput,
} from "@aws-sdk/client-s3";

const REGION = process.env.AWS_REGION;
const BUCKET_NAME = process.env.BUCKET_NAME;

const s3Client = new S3Client({
    region: REGION,
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
    },
});

export const getFileFromS3 = async (key: string): Promise<string> => {
    try {
        const command = new GetObjectCommand({
            Bucket: BUCKET_NAME,
            Key: key,
        });

        const response: GetObjectCommandOutput = await s3Client.send(command);

        if (!response.Body) {
            throw new Error("File not found or empty response.");
        }

        const body = response.Body as ReadableStream;
        const chunks: Uint8Array[] = [];
        const reader = body.getReader();

        let done = false;
        while (!done) {
            const { value, done: readerDone } = await reader.read();
            if (readerDone) {
                done = true;
                break;
            }
            if (value) {
                chunks.push(value);
            }
        }

        const blob = new Blob(chunks);
        return URL.createObjectURL(blob);
    } catch (error) {
        console.error("Error retrieving file from S3:", error);
        throw error;
    }
};

