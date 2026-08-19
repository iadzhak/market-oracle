const baseUrl = 'http://127.0.0.1:8000';
export const tokensUrl = new URL('/api/tokens', baseUrl);

export function forecastUrl(token: string): URL {
  return new URL(`/api/tokens/${token}`, baseUrl);
}