module.exports = {
  apps : [{
    name   : "comentador-linkedin",
    script : "main.py",
    interpreter: "./venv/Scripts/python.exe",
    env_production: {
      ENVIRONMENT: "production",
      // Carrega variáveis do arquivo .env
      env_file: ".env.prod"
    },
  }]
}