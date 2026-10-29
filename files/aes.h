/**
 * @file aes.h
 * @brief AES-128 block decryption + RFC 3394 AES Key Unwrap
 */
#ifndef _AES_H_
#define _AES_H_

#include <stdint.h>

/* Decrypt one 16-byte block in place with a 128-bit key. */
void aes128_decrypt_block(const uint8_t *key, uint8_t block[16]);

/**
 * RFC 3394 AES Key Unwrap with a 128-bit KEK.
 * Unwraps "len" bytes of "data" (len = 8*(n+1), n>=1) into "out".
 * Returns the payload length (len-8) on success, -1 on integrity failure.
 */
int32_t aes_kw_unwrap(const uint8_t kek[16], uint8_t *data, uint32_t len, uint8_t *out);

#endif
