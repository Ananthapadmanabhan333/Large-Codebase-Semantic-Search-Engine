# Aether Intelligence - Environment Setup Script (Windows)

Write-Host "🌌 Initializing Aether Intelligence Platform Setup..." -ForegroundColor Cyan

# 1. Create Storage Directories
New-Item -ItemType Directory -Path ./storage/repos -Force | Out-Null
Write-Host "✅ Created storage directories."

# 2. Check for Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker found."
} else {
    Write-Warning "⚠️ Docker not found. Please install Docker Desktop to run the infrastructure."
}

# 3. Create .env if not exists
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ Created .env from .env.example. PLEASE UPDATE YOUR OPENAI_API_KEY." -ForegroundColor Yellow
}

# 4. Instructions
Write-Host "`n🚀 Setup Complete! Follow these steps to launch:" -ForegroundColor Green
Write-Host "1. Update .env with your credentials."
Write-Host "2. Run 'docker-compose -f infra/docker/docker-compose.yml up -d' to start the stack."
Write-Host "3. Start the backend: cd apps/api; pip install -r requirements.txt; python main.py"
Write-Host "4. Start the frontend: cd apps/web; npm install; npm run dev"
Write-Host "`nHappy Coding! 🛸"
