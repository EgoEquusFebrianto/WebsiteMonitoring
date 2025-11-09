import prisma from '../prisma/client.js';

export async function getLatestNetworkEvents(model = "lr", lastOffset = -1, limit = 100) {
  const tableName = `networkEvent_${model}`;
  
  return prisma[tableName].findMany({
    where: {
      stream_offset: lastOffset,
    },
    orderBy: { stream_offset: "asc" }, // pastikan urutan naik sesuai offset
    take: limit,
  });
}