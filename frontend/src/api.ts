export const tokensUrl = '/api/tokens';

export function forecastUrl(token: string): string {
  return `/api/tokens/${token}`;
}