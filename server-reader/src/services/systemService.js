import prisma from '../prisma/client.js';

export async function getLatestSystemPerformance(limit = 10) {
  return prisma.systemPerformance_lr.findMany({
    orderBy: { timestamp: "desc" },
    take: limit,
  });
}
