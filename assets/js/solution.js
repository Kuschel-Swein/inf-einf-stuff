const encoder = new TextEncoder();
const decoder = new TextDecoder();

const decodeFromUtf8 = data => decoder.decode(data);
const encodeToUtf8 = data => encoder.encode(data);

const decodeFromBase64 = base64 =>
    Uint8Array.from(atob(base64), c => c.charCodeAt(0));
const encodeToBase64 = buffer =>
    btoa(
        new Uint8Array(buffer).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ''
        )
    );

async function importKey(key) {
    const keyMaterial = encodeToUtf8(key);

    return crypto.subtle.importKey('raw', keyMaterial, 'PBKDF2', false, [
        'deriveKey',
    ]);
}

async function deriveKey(passwordKey, salt, usage) {
    return crypto.subtle.deriveKey(
        { name: 'PBKDF2', salt, iterations: 250_000, hash: 'SHA-256' },
        passwordKey,
        { name: 'AES-GCM', length: 256 },
        false,
        [usage]
    );
}

export async function encrypt(password, plainText) {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv = crypto.getRandomValues(new Uint8Array(12)); // random, 96-bit IV

    const passwordKey = await importKey(password);
    const key = await deriveKey(passwordKey, salt, 'encrypt');

    const cipherText = new Uint8Array(
        await crypto.subtle.encrypt(
            {
                name: 'AES-GCM',
                iv,
            },
            key,
            encodeToUtf8(plainText)
        )
    );

    const payload = new Uint8Array(
        salt.byteLength + iv.byteLength + cipherText.byteLength
    );

    payload.set(salt, 0);
    payload.set(iv, salt.byteLength);
    payload.set(cipherText, salt.byteLength + iv.byteLength);

    return encodeToBase64(payload);
}

export async function decrypt(password, payloadText) {
    const payload = decodeFromBase64(payloadText);

    const salt = payload.slice(0, 16);
    const iv = payload.slice(16, 16 + 12);
    const cipherText = payload.slice(16 + 12);

    const passwordKey = await importKey(password);
    const key = await deriveKey(passwordKey, salt, 'decrypt');

    const plainText = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv },
        key,
        cipherText
    );

    return decodeFromUtf8(plainText);
}
