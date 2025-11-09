import prisma from '../prisma/client.js';

export async function getLatestAttackSummary(model = "lr", lastOffset, limit = 1) {
  const tableName = `attackSummary_${model}`;

  return prisma[tableName].findMany({
    where: {
      stream_offset: lastOffset,
    },
    orderBy: { stream_offset: "asc" }, // pastikan urutan naik
    take: limit,
  });
}