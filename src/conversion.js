/**
 * MHS2 Save Transfer Logic
 * Based on research by AsteriskAmpersand and Andoryuuta
 */
import { GUI_MESSAGE_TABLE_IDS } from './gui_table.js';
import { Blowfish } from './blowfish.js';
import { SeededXorshift128 } from './xorshift128.js';

// ============================================================================
// Constants
// ============================================================================
const HEADER_SIZE = 0x30;
const SHA_START = 0x40;
const STEAM_ID_LOC = 8407304;
const FILE_SIZE_PC = 8421552;
const FILE_SIZE_NSW = 8421496;
const STEAM_ID_64_BASE = 76561197960265728n;

// ============================================================================
// Key Generation
// ============================================================================
function getSaveSeedForSteamID(steamID32) {
    return GUI_MESSAGE_TABLE_IDS[steamID32 % (GUI_MESSAGE_TABLE_IDS.length - 1)];
}

export function getSaveBlowfishKeyForSteamID(steamID32) {
    const saveSeed = getSaveSeedForSteamID(steamID32);
    const rng = new SeededXorshift128();
    rng.init(saveSeed >>> 0);

    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";

    let key = '';
    for (let i = 0; i < 56; i++) {
        key += alphabet[Math.abs(rng.nextRand()) % alphabet.length];
    }
    return key;
}

export function steamID64To32(steamID64) {
    return Number(BigInt(steamID64) - STEAM_ID_64_BASE);
}

// ============================================================================
// CRC-32 (JamCrc)
// ============================================================================
const CRC_TABLE = (() => {
    const table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
        let c = n;
        for (let k = 0; k < 8; k++) {
            c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        }
        table[n] = c >>> 0;
    }
    return table;
})();

function crc32(data) {
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < data.length; i++) {
        crc = (CRC_TABLE[(crc ^ data[i]) & 0xFF] ^ (crc >>> 8)) >>> 0;
    }
    return (crc ^ 0xFFFFFFFF) >>> 0;
}

// ============================================================================
// SHA-1 (Pure JS)
// ============================================================================
function sha1(data) {
    const h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0];

    // Pad to 64-byte boundary
    const len = data.length;
    const paddedLen = Math.ceil((len + 9) / 64) * 64;
    const padded = new Uint8Array(paddedLen);
    padded.set(data);
    padded[len] = 0x80;

    // Write bit length (big-endian)
    const bitLen = BigInt(len * 8);
    const view = new DataView(padded.buffer);
    view.setBigUint64(paddedLen - 8, bitLen, false);

    for (let chunk = 0; chunk < paddedLen; chunk += 64) {
        const w = new Uint32Array(80);
        const chunkView = new DataView(padded.buffer, chunk, 64);
        for (let i = 0; i < 16; i++) {
            w[i] = chunkView.getUint32(i * 4, false);
        }
        for (let i = 16; i < 80; i++) {
            w[i] = rotl32(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1);
        }

        let [a, b, c, d, e] = h;

        for (let i = 0; i < 80; i++) {
            let f, k;
            if (i < 20) {
                f = (b & c) | (~b & d);
                k = 0x5A827999;
            } else if (i < 40) {
                f = b ^ c ^ d;
                k = 0x6ED9EBA1;
            } else if (i < 60) {
                f = (b & c) | (b & d) | (c & d);
                k = 0x8F1BBCDC;
            } else {
                f = b ^ c ^ d;
                k = 0xCA62C1D6;
            }

            const temp = (rotl32(a, 5) + f + e + k + w[i]) >>> 0;
            e = d;
            d = c;
            c = rotl32(b, 30);
            b = a;
            a = temp;
        }

        h[0] = (h[0] + a) >>> 0;
        h[1] = (h[1] + b) >>> 0;
        h[2] = (h[2] + c) >>> 0;
        h[3] = (h[3] + d) >>> 0;
        h[4] = (h[4] + e) >>> 0;
    }

    const result = new Uint8Array(20);
    const resView = new DataView(result.buffer);
    for (let i = 0; i < 5; i++) {
        resView.setUint32(i * 4, h[i], false);
    }
    return result;
}

function rotl32(x, n) {
    return ((x << n) | (x >>> (32 - n))) >>> 0;
}

// ============================================================================
// Endianness Reversal
// ============================================================================
function endiannessReversal(data) {
    const chunks = [];
    for (let i = 0; i < data.length; i += 4) {
        chunks.push(new Uint8Array(data.slice(i, i + 4)).reverse());
    }
    return new Uint8Array(chunks.flat());
}

// ============================================================================
// Blowfish Capcom Style
// ============================================================================
function capcomDecrypt(fileData, keyString) {
    const keyBytes = new Uint8Array(keyString.split('').map(c => c.charCodeAt(0)));
    const bf = new Blowfish(keyBytes);
    const reversed = endiannessReversal(fileData);
    const decrypted = bf.decryptECB(reversed);
    return endiannessReversal(decrypted);
}

function capcomEncrypt(fileData, keyString) {
    const keyBytes = new Uint8Array(keyString.split('').map(c => c.charCodeAt(0)));
    const bf = new Blowfish(keyBytes);
    const reversed = endiannessReversal(fileData);
    const encrypted = bf.encryptECB(reversed);
    return endiannessReversal(encrypted);
}

// ============================================================================
// Header Building
// ============================================================================
const PREAMBLE = new Uint8Array([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00]);
const MID = new Uint8Array([0x70, 0x80, 0x80, 0x00]);
const EPILOGUE = new Uint8Array([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]);

function buildHeader(body, pckey) {
    const keyBytes = new TextEncoder().encode(pckey);
    const crc = crc32(keyBytes);
    const keyCrc = new Uint8Array([crc & 0xFF, (crc >> 8) & 0xFF, (crc >> 16) & 0xFF, (crc >> 24) & 0xFF]);

    const shaHash = sha1(body.slice(SHA_START));

    const header = new Uint8Array(HEADER_SIZE);
    header.set(PREAMBLE, 0);
    header.set(shaHash, 0x0C);
    header.set(MID, 0x20);
    header.set(keyCrc, 0x24);
    header.set(EPILOGUE, 0x28);

    return header;
}

function replaceHeader(body, pckey) {
    const newHeader = buildHeader(body, pckey);
    const result = new Uint8Array(body.length);
    result.set(newHeader, 0);
    result.set(body.slice(HEADER_SIZE), HEADER_SIZE);
    return result;
}

// ============================================================================
// Steam ID Insertion
// ============================================================================
function insertSteamID(body, steamId32) {
    const result = new Uint8Array(body.length);
    result.set(body, 0);
    const view = new DataView(result.buffer);
    view.setUint32(STEAM_ID_LOC, steamId32, true);
    return result;
}

function steamTransfer(body, pckey, steamId32) {
    let data = insertSteamID(body, steamId32);
    data = replaceHeader(data, pckey);
    return data;
}

// ============================================================================
// Key Detection
// ============================================================================
// We generate keys on-the-fly for each SteamID32 and try decryption of the last 8 bytes
// If sum of decrypted bytes is 0, it's the correct key

function tryDetectKey(eBody) {
    const testArea = eBody.slice(-8);
    
    // Try a range of Steam IDs (this is a simplified approach)
    // In practice, we can try a few hundred Steam IDs to find the right key
    // The original tool had pre-computed keys
    
    // For very fast detection, we'll iterate from Steam ID 0 upward
    // Most users will have low Steam IDs
    for (let steamId32 = 0; steamId32 < 1000; steamId32++) {
        const key = getSaveBlowfishKeyForSteamID(steamId32);
        const bf = new Blowfish(new TextEncoder().encode(key));
        const reversed = endiannessReversal(testArea);
        const decrypted = bf.decryptECB(reversed);
        const sum = decrypted.reduce((a, b) => a + b, 0);
        if (sum === 0) {
            return { key, steamId32 };
        }
    }
    throw new Error('Could not detect encryption key');
}

// ============================================================================
// File Operations
// ============================================================================

export async function filePCtoPC(inputBuffer, targetSteamId64) {
    const inputData = new Uint8Array(inputBuffer);
    const targetSteamId32 = steamID64To32(targetSteamId64);

    // Detect the encryption key
    const { key: inkey, steamId32: sourceSteamId32 } = tryDetectKey(inputData);
    
    // Decrypt with original key
    const dBody = capcomDecrypt(inputData, inkey);

    // Get new key for target Steam ID
    const pckey = getSaveBlowfishKeyForSteamID(targetSteamId32);

    // Transfer to new account
    const dOut = steamTransfer(dBody, pckey, targetSteamId32);

    // Encrypt with new key
    const eOut = capcomEncrypt(dOut, pckey);

    return eOut;
}

export async function fileNSWtoPC(inputBuffer, targetSteamId64) {
    const switchData = new Uint8Array(inputBuffer);
    const targetSteamId32 = steamID64To32(targetSteamId64);

    // Get the key for target
    const pckey = getSaveBlowfishKeyForSteamID(targetSteamId32);

    // Build PC skeleton from NSW format
    const skeleton = new Uint8Array(HEADER_SIZE + switchData.length + 8);
    skeleton.set(switchData.slice(0, 0xC), 0);
    skeleton.set(switchData.slice(0xC), 0xC + HEADER_SIZE);
    skeleton.set(EPILOGUE, 0xC + HEADER_SIZE + switchData.length);

    const dBody = steamTransfer(skeleton, pckey, targetSteamId32);
    const eBody = capcomEncrypt(dBody, pckey);

    return eBody;
}

export async function filePCtoNSW(inputBuffer) {
    const pcData = new Uint8Array(inputBuffer);

    // Find the key
    const { key: inkey } = tryDetectKey(pcData);
    const dBody = capcomDecrypt(pcData, inkey);

    // Convert to NSW format - remove PC header and epilogue
    const nswData = new Uint8Array(dBody.length - HEADER_SIZE - 8);
    nswData.set(dBody.slice(0xC, -8));

    return nswData;
}

// ============================================================================
// Main Convert Function
// ============================================================================
export async function convertSave(fileBuffer, options) {
    const { targetSteamId, convertToSwitch } = options;
    const fileSize = fileBuffer.byteLength;

    if (convertToSwitch) {
        if (fileSize !== FILE_SIZE_PC) {
            throw new Error('Input file is not a PC save file (expected ' + FILE_SIZE_PC + ' bytes, got ' + fileSize + ')');
        }
        return await filePCtoNSW(fileBuffer);
    } else {
        if (fileSize === FILE_SIZE_PC) {
            return await filePCtoPC(fileBuffer, targetSteamId);
        } else if (fileSize === FILE_SIZE_NSW) {
            return await fileNSWtoPC(fileBuffer, targetSteamId);
        } else {
            throw new Error('Unrecognized save file format (expected ' + FILE_SIZE_PC + ' or ' + FILE_SIZE_NSW + ' bytes, got ' + fileSize + ')');
        }
    }
}