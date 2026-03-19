// Credenciais hardcoded espalhadas e expostas
const config = {
    dbUser: "admin_master",
    dbPass: "senha_super_secreta_prod_123", 
    paymentGatewayKey: "pk_live_1234567890abcdef",
    smtpUser: "no-reply@fullcycle.com.br",
    port: 3000
};

// Global state perigoso: cache em memória que vai vazar dados entre requisições
let globalCache = {};
let totalRevenue = 0; // Acoplamento de estado global

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}

// Função síncrona bloqueante simulando um hash ruim
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}

module.exports = { config, logAndCache, badCrypto, globalCache, totalRevenue };