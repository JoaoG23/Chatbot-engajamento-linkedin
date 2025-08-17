module.exports = {
  apps : [{
    name   : "comentador-linkedin",
    script : "main.py",
    interpreter: "python",
    env_production: {
      ENVIRONMENT: "production",
      // Carrega variáveis do arquivo .env
      env_file: "prod.env"
    },
  }]
}