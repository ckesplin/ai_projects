/**
 * Seeded Xorshift128 PRNG
 * Port from Andoryuuta's C++ implementation
 * https://github.com/Andoryuuta/MHS2SaveKeygen
 */
export class SeededXorshift128 {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.z = 0;
        this.w = 0;
    }

    init(seed) {
        this.x = 123456789;
        this.y = 362436069;
        this.z = 521288629;
        this.w = 88675123;

        let v2 = 0x159A55E5;
        let v3 = 521288629;
        let v4 = 88675123;
        let v5 = seed ^ 0xAC9365;

        for (let i = 0; i < 100; i++) {
            const v7 = v2;
            v2 = v3;
            v3 = v4;
            v5 ^= (0x65AC9365 >>> (v5 & 3)) ^ ((v5 ^ (0x65AC9365 >>> (v5 & 3))) >>> 3) 
                 ^ ((v5 ^ (0x65AC9365 >>> (v5 & 3))) >>> 4) ^ (8 * (v5 ^ (0x65AC9365 >>> (v5 & 3)))) 
                 ^ (16 * (v5 ^ (0x65AC9365 >>> (v5 & 3))));
            v4 ^= v5 ^ (v5 << 15) ^ ((v5 ^ (v5 << 15)) >>> 4) ^ (v4 >>> 21);
        }

        this.x = v7;
        this.y = v2;
        this.z = v3;
        this.w = v4;
    }

    nextRand() {
        const t = this.x ^ (this.x << 15);
        this.x = this.y;
        this.y = this.z;
        this.z = this.w;
        this.w = t ^ this.w ^ ((t ^ (this.w >>> 17)) >>> 4);
        return this.w;
    }
}