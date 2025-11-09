/*
  Warnings:

  - You are about to drop the column `offset` on the `AttackSummary_lr` table. All the data in the column will be lost.
  - You are about to drop the column `offset` on the `AttackSummary_rf` table. All the data in the column will be lost.
  - You are about to drop the column `offset` on the `NetworkEvent_lr` table. All the data in the column will be lost.
  - You are about to drop the column `offset` on the `NetworkEvent_rf` table. All the data in the column will be lost.
  - Added the required column `stream_offset` to the `AttackSummary_lr` table without a default value. This is not possible if the table is not empty.
  - Added the required column `stream_offset` to the `AttackSummary_rf` table without a default value. This is not possible if the table is not empty.
  - Added the required column `stream_offset` to the `NetworkEvent_lr` table without a default value. This is not possible if the table is not empty.
  - Added the required column `stream_offset` to the `NetworkEvent_rf` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "AttackSummary_lr" DROP COLUMN "offset",
ADD COLUMN     "stream_offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "AttackSummary_rf" DROP COLUMN "offset",
ADD COLUMN     "stream_offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "NetworkEvent_lr" DROP COLUMN "offset",
ADD COLUMN     "stream_offset" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "NetworkEvent_rf" DROP COLUMN "offset",
ADD COLUMN     "stream_offset" INTEGER NOT NULL;
