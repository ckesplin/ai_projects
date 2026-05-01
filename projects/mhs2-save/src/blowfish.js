/**
 * Blowfish ECB Implementation
 * Wraps blowfish-js package for correct encryption
 */
import bf from 'blowfish-js';

const { key: blfKey, ecb } = bf;

export class Blowfish {
    constructor(keyInput) {
        if (typeof keyInput === 'string') {
            this.key = Buffer.from(keyInput);
        } else {
            this.key = Buffer.from(keyInput);
        }
        this._state = blfKey(this.key);
    }

    encryptBlock(xl, xr) {
        const [L, R] = bf.encipherBlock(this._state, xl, xr);
        return [R, L];
    }

    decryptBlock(xl, xr) {
        const [L, R] = bf.decipherBlock(this._state, xl, xr);
        return [R, L];
    }

    encryptECB(data) {
        const buf = Buffer.from(data);
        return new Uint8Array(ecb(this._state, buf, false));
    }

    decryptECB(data) {
        const buf = Buffer.from(data);
        return new Uint8Array(ecb(this._state, buf, true));
    }
}
