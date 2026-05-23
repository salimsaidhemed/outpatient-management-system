import Keycloak from 'keycloak-js'

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8080',
  realm: import.meta.env.VITE_KEYCLOAK_REALM || 'outpatient',
  clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'admissions-frontend',
})

let initPromise

export function initAuth() {
  if (!initPromise) {
    initPromise = keycloak.init({
      pkceMethod: 'S256',
      checkLoginIframe: false,
    })
  }
  return initPromise
}

export function login() {
  return keycloak.login({ redirectUri: window.location.href })
}

export function logout() {
  return keycloak.logout({ redirectUri: window.location.origin })
}

export async function getToken() {
  if (!keycloak.authenticated) return null
  await keycloak.updateToken(30)
  return keycloak.token
}

export function getUserProfile() {
  return {
    authenticated: Boolean(keycloak.authenticated),
    username: keycloak.tokenParsed?.preferred_username || '',
    name: keycloak.tokenParsed?.name || keycloak.tokenParsed?.preferred_username || '',
    email: keycloak.tokenParsed?.email || '',
    roles: keycloak.tokenParsed?.realm_access?.roles || [],
  }
}
