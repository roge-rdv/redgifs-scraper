#!/usr/bin/env node

import fs from "fs";
import { getGif } from "redgif";
import path from "path";

const link = process.argv[2]; // Recebe o link como argumento
if (!link) {
  console.error("Nenhum link fornecido.");
  process.exit(1);
}

const regex = /https:\/\/www\.redgifs\.com\/watch\/(\w+)/;
const match = link.match(regex);

if (match) {
  const gifId = match[1];
  console.log(`Downloading ${gifId}...`);

  // Diretório para salvar os vídeos
  const downloadsDir = path.join(process.cwd(), "downloads"); // Certifique-se de usar o diretório correto
  console.log(`Salvando no diretório: ${downloadsDir}`);
  if (!fs.existsSync(downloadsDir)) {
    fs.mkdirSync(downloadsDir);
  }

  const outputPath = path.join(downloadsDir, `${gifId}.mp4`);

  // Verifica se o vídeo já foi baixado
  if (fs.existsSync(outputPath)) {
    console.log(`Vídeo já baixado: ${outputPath}`);
    process.exit(0);
  }

  // Baixa o vídeo
  getGif(gifId)
    .then((data) => {
      fs.writeFileSync(outputPath, data);
      console.log(`Vídeo salvo em: ${outputPath}`);
    })
    .catch((error) => {
      console.error(`Erro ao baixar o vídeo ${gifId}:`, error.message);
      process.exit(1);
    });
} else {
  console.error("Link inválido.");
  process.exit(1);
}
