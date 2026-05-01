/**
 * Blowfish ECB Implementation
 * Pure JavaScript port - no external dependencies
 * 
 * Reference: Bruce Schneier's Blowfish algorithm
 * Used by Monster Hunter Stories 2 for save file encryption
 */

function F(S, x) {
    return (
        ((S[0][(x >>> 24) & 0xFF] + S[1][(x >>> 16) & 0xFF]) ^ S[2][(x >>> 8) & 0xFF]) + S[3][x & 0xFF]
    );
}

function encryptBlock(xl, xr, P, S) {
    for (let i = 0; i < 16; i += 2) {
        xl ^= P[i];
        xr ^= F(S, xl);
        xr ^= P[i + 1];
        xl ^= F(S, xr);
    }
    xl ^= P[16];
    xr ^= P[17];
    return [xr, xl]; // Swap and return
}

export class Blowfish {
    constructor(key) {
        // Convert string key to bytes if needed
        if (typeof key === 'string') {
            this.key = new Uint8Array(key.split('').map(c => c.charCodeAt(0)));
        } else {
            this.key = key;
        }
        const { S, P } = this._generateSBoxes(this.key);
        this.S = S;
        this.P = P;
    }

    _generateSBoxes(key) {
        const S = [
            new Uint32Array(256),
            new Uint32Array(256),
            new Uint32Array(256),
            new Uint32Array(256)
        ];
        const P = new Uint32Array(18);

        // Initialize S-boxes with digits of pi
        const pi = [
            0x3243F6A8, 0x885A308D, 0x313198A2, 0xE0370734,
            0x40902260, 0xD63A0315, 0xE051C14C, 0xD2AA120F,
            0x29663949, 0xE0FAF757, 0x18DC9EB3, 0x37C2E0B5,
            0xCF05DAF0, 0x4EB3E804, 0x9B5C86A9, 0x16652215,
            0x13B5B0A5, 0x372D2F68, 0xFA59C4C3, 0xC67CE57A,
            0xF8CD75D3, 0x6FBAA3E5, 0xA78F1D45, 0x9CAA3A1E,
            0x2B5BDBF2, 0x1CA6788E, 0xA167EF93, 0x4D2F1D46,
            0xDF9A8678, 0xABFA45B4, 0x6C3E97D0, 0x8D0DB87A,
            0x6E9D0F48, 0x0A42E46F, 0x6F0FEBB7, 0x3E8F11C7,
            0xB6BAB6E1, 0x79C4D1A5, 0xC20D7E6B, 0xA6A32B3B,
            0x5B4F3A8C, 0xFBB6BDFD, 0x4BDEEB49, 0x53A8A5A6,
            0x6BB0D3B0, 0xA86BA620, 0xD6D6E19B, 0x5D0C3E42,
            0xEE2C71F2, 0xFA459A4C, 0xA2EBAE4C, 0x5D4EFD5F,
            0xE6F84A0F, 0x5A68C4B2, 0xDAD5F25B, 0xABD3FAEF,
            0xB58D7FE0, 0xB2A12B68, 0x5B7BCE1B, 0xB4D5BD7F,
            0x3F7D8C5C, 0xD2CFE6F3, 0xA6D0CE0E, 0x8B2DE689,
            0xB5F8FA9D, 0x4F11A9F5, 0x7BA7E3DE, 0x2D0EAFA3,
            0xF57C8B0E, 0x4D9B6380, 0xC7AEEC54, 0xEA2C0EE2,
            0xD9EEA9A7, 0xDB23E3D7, 0x6E5B2EA7, 0xD77C1D53,
            0x1DBB2F2A, 0x4EA7B20F, 0xAF59B82F, 0xDBA72F71,
            0x5E0A1B5C, 0x0BCF99F3, 0xD1E4D7B6, 0x6F9FFAD2,
            0xACAF6E5A, 0x1E3EBF1D, 0xF6E71D4F, 0x5A7BABF3,
            0xC0F9FA96, 0x2DF0F0A6, 0xD2EE4DF9, 0x2CFEDE40,
            0x9AADEE91, 0xA0EBEE8E, 0xDE4E8D96, 0xD4E2E8D4,
            0xD0B5EA2A, 0xA1EAE6BD, 0xE2DAE5B3, 0xBBE1E7D5,
            0xE4E9DBB6, 0x5C82ED83, 0x6CB4BFBB, 0x9EB5EDDF,
            0xFFEDCBA8, 0xBCBCE8C9, 0xD2D0D8DA, 0xD6D0DAD5,
            0xD0D2D6DE, 0xD4D7E3D9, 0xC0D1D0D5, 0xD9D4DCCD,
            0xD7D6E6C2, 0xD4C0CFDB, 0xBFCAC9CC, 0xCACEC4C1,
            0xCBCAC8C9, 0xC9D1C4CF, 0xD2D7D5CF, 0xCDCCDBD8,
            0xCCD4CDC9, 0xCDD0D6D9, 0xD6CFDBDF, 0xD3D4DAE0,
            0xD4DAD7E1, 0xD6E4D5E3, 0xE0D4D9E8, 0xDDE5D6D9,
            0xDEDAD5DE, 0xDCD9D7E0, 0xDCD6D4DC, 0xD5D0D1D8,
            0xCAC8CCD0, 0xCACCCACF, 0xCDC6CACB, 0xCAC8C6CA,
            0xBCC8CAC3, 0xBCC8C4BF, 0xBFC9C4C3, 0xBCC8BCC3,
            0xBEC0C0C0, 0xBFC2C4BE, 0xC3C6C4C3, 0xBBC4BFBD,
            0xBBBEC2BA, 0xB9BBC3BC, 0xBEBFC1BD, 0xB9B7B7BB,
            0xBABBB9BA, 0xB7B6B8B7, 0xB5B6B4B6, 0xB4B5B3B5,
            0xB2B0B1B2, 0xAEB1AEB0, 0xAEB1ADAF, 0xACAAACAE,
            0xAAA8AAAB, 0xA8A7A9A8, 0xA6A7A6A6, 0xA6A5A5A6,
            0xA3A4A4A4, 0xA3A3A4A3, 0xA1A2A3A1, 0xA0A1A1A0,
            0x9FA09FA0, 0x9E9E9F9E, 0x9C9D9E9C, 0x9B9B9C9B,
            0x99999A99, 0x98989998, 0x96979896, 0x95959695,
            0x93949593, 0x92929392, 0x90919290, 0x8F8F908F,
            0x8D8E8F8D, 0x8C8D8C8C, 0x8A8B8C8A, 0x89898A89,
            0x87888887, 0x86878786, 0x84858684, 0x84848584,
            0x82838482, 0x81828381, 0x7F80817F, 0x7E7F807E,
            0x7C7D7E7C, 0x7B7C7D7B, 0x797A7B79, 0x78797878,
            0x76777876, 0x75767775, 0x73747573, 0x73737473,
            0x71727371, 0x70717270, 0x6E6F706E, 0x6D6E6F6D,
            0x6B6C6D6B, 0x6A6B6C6A, 0x68696A68, 0x67686967,
            0x65666765, 0x64656664, 0x62636462, 0x61626361,
            0x5F60615F, 0x5E5F605E, 0x5C5D5E5C, 0x5B5C5D5B,
            0x595A5B59, 0x58595858, 0x56575856, 0x55565755,
            0x53545553, 0x52535452, 0x50515250, 0x4F50514F,
            0x4D4E4F4D, 0x4C4D4E4C, 0x4A4B4C4A, 0x494A4B49,
            0x47484947, 0x46474846, 0x44454644, 0x43444543,
            0x41424341, 0x40414240, 0x3E3F403E, 0x3D3E3F3D,
            0x3B3C3D3B, 0x3A3B3C3A, 0x38393A38, 0x37383737,
            0x35363735, 0x34353634, 0x32333432, 0x31323331,
            0x2F30312F, 0x2E2F302E, 0x2C2D2E2C, 0x2B2C2D2B,
            0x292A2B29, 0x28292828, 0x26272826, 0x25262725,
            0x23242523, 0x22232422, 0x20212220, 0x1F20211F,
            0x1D1E1F1D, 0x1C1D1E1C, 0x1A1B1C1A, 0x191A1B19,
            0x17181917, 0x16171816, 0x14151614, 0x13141513,
            0x11121311, 0x10111210, 0x0E0F100E, 0x0D0E0F0D,
            0x0B0C0D0B, 0x0A0B0C0A, 0x08090A08, 0x07080907,
            0x05060705, 0x04050604, 0x02030402, 0x01020301,
            0x00010200, 0x01000100, 0xFFFFFF00, 0xFFFFFFFF
        ];

        // Expand S-boxes with pi digits
        let idx = 0;
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 256; j++) {
                S[i][j] = pi[idx++];
            }
        }

        // Initialize P-array with first 18 digits of pi
        const pInit = [0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89, 0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C, 0xC0AC29B7, 0xC97C0925, 0xD1CF0853, 0x9B64C2B0, 0x512E9E86, 0x3F84D5B5];
        for (let i = 0; i < 18; i++) {
            P[i] = pInit[i];
        }

        // XOR key into P-array (key is up to 56 bytes = 448 bits)
        let keyIdx = 0;
        for (let i = 0; i < 18; i++) {
            const val = (
                (key[keyIdx % key.length] << 24) |
                (key[(keyIdx + 1) % key.length] << 16) |
                (key[(keyIdx + 2) % key.length] << 8) |
                key[(keyIdx + 3) % key.length]
            );
            P[i] ^= val;
            keyIdx += 4;
        }

        // Encrypt all-zero block with current P-array and S-boxes, update P and S
        let xl = 0, xr = 0;

        for (let i = 0; i < 18; i += 2) {
            const encrypted = encryptBlock(xl, xr, P, S);
            xl = encrypted[0];
            xr = encrypted[1];
            P[i] = xl;
            P[i + 1] = xr;
        }

        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 256; j += 2) {
                const encrypted = encryptBlock(xl, xr, P, S);
                xl = encrypted[0];
                xr = encrypted[1];
                S[i][j] = xl;
                S[i][j + 1] = xr;
            }
        }

        return { S, P };
    }

    encryptBlock(xl, xr) {
        for (let i = 0; i < 16; i += 2) {
            xl ^= this.P[i];
            xr ^= F(this.S, xl);
            xr ^= this.P[i + 1];
            xl ^= F(this.S, xr);
        }
        xl ^= this.P[16];
        xr ^= this.P[17];
        return [xr, xl]; // Swap and return
    }

    decryptBlock(xl, xr) {
        for (let i = 17; i > 1; i -= 2) {
            xl ^= this.P[i];
            xr ^= F(this.S, xl);
            xr ^= this.P[i - 1];
            xl ^= F(this.S, xr);
        }
        xl ^= this.P[0];
        xr ^= this.P[1];
        return [xr, xl]; // Swap and return
    }

    encryptECB(data) {
        // Data must be multiple of 8 bytes
        const result = new Uint8Array(data.length);
        for (let i = 0; i < data.length; i += 8) {
            const block = new Uint8Array(data.slice(i, i + 8));
            const view = new DataView(block.buffer);
            let xl = view.getUint32(0, false);
            let xr = view.getUint32(4, false);
            const [encL, encR] = this.encryptBlock(xl, xr);
            const outView = new DataView(result.buffer, i, 8);
            outView.setUint32(0, encL, false);
            outView.setUint32(4, encR, false);
        }
        return result;
    }

    decryptECB(data) {
        const result = new Uint8Array(data.length);
        for (let i = 0; i < data.length; i += 8) {
            const block = new Uint8Array(data.slice(i, i + 8));
            const view = new DataView(block.buffer);
            let xl = view.getUint32(0, false);
            let xr = view.getUint32(4, false);
            const [decL, decR] = this.decryptBlock(xl, xr);
            const outView = new DataView(result.buffer, i, 8);
            outView.setUint32(0, decL, false);
            outView.setUint32(4, decR, false);
        }
        return result;
    }
}
