$ErrorActionPreference = "Stop"

$containerName = "portfolio-pgvector"
$existing = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"

if ($existing -eq $containerName) {
    docker start $containerName | Out-Null
    Write-Output "$containerName started"
} else {
    docker run -d `
        --name $containerName `
        -p 5434:5432 `
        -e POSTGRES_DB=portfolio_db `
        -e POSTGRES_USER=portfolio_user `
        -e POSTGRES_PASSWORD=portfolio_password `
        -v portfolio-pgvector-data:/var/lib/postgresql/data `
        pgvector/pgvector:pg16 | Out-Null
    Write-Output "$containerName created"
}

docker ps --filter "name=^/$containerName$" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

